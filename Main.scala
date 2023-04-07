import org.apache.spark
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.feature.{OneHotEncoder, StringIndexer, VectorAssembler}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.catalyst.dsl.expressions.StringToAttributeConversionHelper
import org.apache.spark.sql.functions.current_date
import shapeless.syntax.std.tuple.unitTupleOps
//import org.apache.spark.sql.functions.{col, dayofmonth, dayofweek, hour, month, to_date, year, months_between, fil}
import org.apache.spark.sql.functions._

import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.evaluation.BinaryClassificationEvaluator
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.tuning.{ParamGridBuilder, TrainValidationSplit}

object Main {
  def main(args: Array[String]): Unit = {
    println("Hello world!")
    val spark = SparkSession.builder()
      .appName("My Spark Application")
      .master("local[*]")
      .config("spark.driver.bindAddress", "127.0.0.1")
      .getOrCreate()


    // spark code
    var trainDF = spark.read
      .option("header", true)
      .option("inferSchema", true)
      .csv("src/main/scala/fraud-detection/fraudTrain.csv")
      .dropDuplicates()



    val withAgeDF = trainDF
      .withColumn("age", (year(current_date()) - year(col("dob"))))

    // Use StringIndexer to encode the categorical columns
    val indexer1 = new StringIndexer()
      .setInputCol("category")
      .setOutputCol("category_encoded")

    val indexer2 = new StringIndexer()
      .setInputCol("gender")
      .setOutputCol("gender_encoded")
//
    val indexer3 = new StringIndexer()
      .setInputCol("age")
      .setOutputCol("age_encoded")


    val indexedDF = indexer1.fit(withAgeDF)
      .transform(indexer2.fit(withAgeDF)
        .transform(indexer3.fit(withAgeDF)
          .transform(withAgeDF)))

//    val encodedDF = categoryEncoder.fit(indexedDF).transform(genderEncoder.fit(indexedDF).transform(ageEncoder.fit(indexedDF).transform(indexedDF)))

    val inputDF = indexedDF.select("category_encoded", "amt", "gender_encoded", "age_encoded", "is_fraud")

    inputDF.show()
    val y_train = inputDF.select("is_fraud")
    val X_train = inputDF.select("category_encoded", "amt", "gender_encoded", "age_encoded")
    y_train.show()
    X_train.show()

    var testDF = spark.read
      .option("header", true)
      .option("inferSchema", true)
      .csv("src/main/scala/fraud-detection/fraudTest.csv")
      .dropDuplicates()

    val testWithAge = testDF
      .withColumn("age", (year(current_date()) - year(col("dob"))))

    val indexedTest = indexer1.fit(testWithAge)
      .transform(indexer2.fit(testWithAge)
        .transform(indexer3.fit(testWithAge)
          .transform(testWithAge)))

    val inputTestDF = indexedTest.select("category_encoded", "amt", "gender_encoded", "age_encoded", "is_fraud")

    val y_test = inputDF.select("is_fraud")
    val X_test = inputDF.select("category_encoded", "amt", "gender_encoded", "age_encoded")
    y_test.show()
    X_test.show()

//     // Define the feature columns you want to use for training
//     val featureCols = Array("category_encoded", "amt", "gender_encoded", "age_encoded")

//     // Assemble the feature columns into a feature vector column
//     val assembler = new VectorAssembler().setInputCols(featureCols).setOutputCol("features")
//     val trainDataWithFeatures = assembler.transform(X_train)

//     val Array(trainingData, validationData) = trainDataWithFeatures.randomSplit(Array(0.8, 0.2), seed = 12345)

//     // Logistic regression model
//     val lr = new LogisticRegression()
//     val lrModel = lr.fit(trainingData)
//     val predictions = lrModel.transform(validationData)

//     val accuracy = predictions.filter(col("is_fraud") === col("prediction")).count().toDouble / validationData.count()

// //    val accuracy = predictions.filter($"is_fraud" === $"prediction").count().toDouble / X_test.count()
//     println(s"Accuracy: ${accuracy * 100}%")


    spark.stop()
  }
}
