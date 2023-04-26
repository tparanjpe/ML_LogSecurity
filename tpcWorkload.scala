import org.apache.spark.sql.SparkSession
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.feature.{OneHotEncoder, StringIndexer, VectorAssembler}
import org.apache.spark.sql.catalyst.dsl.expressions.StringToAttributeConversionHelper
//import org.apache.spark.sql.functions.current_date
import shapeless.syntax.std.tuple.unitTupleOps
//import org.apache.spark.sql.functions.{col, dayofmonth, dayofweek, hour, month, to_date, year, months_between}
import org.apache.spark.sql.functions._

import org.apache.spark.ml.classification.{LogisticRegression, RandomForestClassifier}
import org.apache.spark.ml.evaluation.BinaryClassificationEvaluator
import org.apache.spark.ml.tuning.{ParamGridBuilder, TrainValidationSplit}

import org.apache.log4j.{Level, Logger}
import org.apache.spark.ml.feature.MinMaxScaler
import org.apache.spark.ml.clustering.KMeans
import org.apache.spark.sql.functions.{col, lit}



object tpcWorkload {
  def main(args: Array[String]): Unit = {
    Logger.getRootLogger.setLevel(Level.ALL) // set the level
    println("Hello world!")
    val spark = SparkSession.builder()
      .appName("CustomerSegmentation")
      .master("local[*]")
      .config("spark.master", "local")
      .config("spark.driver.bindAddress", "127.0.0.1")
      .getOrCreate()

    var order_data = spark.read
      .option("header", true)
      .option("inferSchema", true)
      .csv("src/main/scala/customer_segmentation/order.csv")

    var lineitem_data = spark.read
      .option("header", true)
      .option("inferSchema", true)
      .csv("src/main/scala/customer_segmentation/lineitem.csv")

    var orderreturns_data = spark.read
      .option("header", true)
      .option("inferSchema", true)
      .csv("src/main/scala/customer_segmentation/order_returns.csv")

    val returns_data = lineitem_data
      .join(
        orderreturns_data,
        lineitem_data("li_order_id") === orderreturns_data("or_order_id") &&
          lineitem_data("li_product_id") === orderreturns_data("or_product_id"),
        "left"
      )

    println(returns_data.count())

    val raw_data = returns_data
      .join(
        order_data,
        returns_data("li_order_id") === order_data("o_order_id")
      )

    println(raw_data.show())
    val filled_data = raw_data.na.fill(0.0)

    val inputDF = filled_data.select("o_order_id", "o_customer_sk", "date", "li_product_id", "price", "quantity", "or_return_quantity")
    print(inputDF.show())

    val dataWithNewColumns = inputDF
      .withColumn("invoice_year", year(col("date")))
      .withColumn("row_price", col("quantity") * col("price"))
      .withColumn("return_row_price", col("or_return_quantity")* col("price"))

    print(dataWithNewColumns.show())

    val groups = dataWithNewColumns
      .groupBy(col("o_customer_sk"), col("o_order_id"))
      .agg(
        sum(col("row_price")).alias("row_price"),
        sum(col("return_row_price")).alias("return_row_price"),
        min(col("invoice_year")).alias("invoice_year")
      )
      .withColumn("ratio", col("return_row_price") / col("row_price"))

    val ratio = groups
      .groupBy(col("o_customer_sk"))
      .agg(mean(col("ratio")).alias("return_ratio"))

    val frequency_groups = groups
      .groupBy(col("o_customer_sk"), col("invoice_year"))
      .agg(countDistinct(col("o_order_id")).alias("o_order_id"))
      .select(col("o_customer_sk"), col("invoice_year"), col("o_order_id"))

    val frequency = frequency_groups
      .groupBy(col("o_customer_sk"))
      .agg(mean(col("o_order_id")).alias("frequency"))

    val result = frequency.join(ratio, Seq("o_customer_sk"), "inner")
    print(result.show())


    spark.stop()
  }
}

