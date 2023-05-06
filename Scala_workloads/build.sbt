ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "2.12.16"

libraryDependencies += "org.apache.spark" %% "spark-core" % "3.2.1"
libraryDependencies += "org.apache.spark" %% "spark-sql" % "3.2.1"
libraryDependencies += "org.apache.spark" %% "spark-mllib" % "3.2.0"
libraryDependencies ++= Seq(
  "org.slf4j" % "slf4j-log4j12" % "1.7.30",
  "log4j" % "log4j" % "1.2.17"
)

lazy val root = (project in file("."))
  .settings(
    name := "ML Log Security"
  )
