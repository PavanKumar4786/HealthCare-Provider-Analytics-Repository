import sys
import os
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType



# 1. ENVIRONMENT SETUP

os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jdk-17"
os.environ["SPARK_HOME"] = r"C:\spark-3.5.7-bin-hadoop3\spark-3.5.7-bin-hadoop3"

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


# 2. START SPARK SESSION

spark = SparkSession.builder \
    .appName("Hospital Insights") \
    .getOrCreate()

print("\n Spark Session Started Successfully!\n")


# 3. LOAD DATASETS

apollo_path = r"C:/Users/PAVAN KUMAR REDDY/Desktop/Revature Training/week-4/spark/datasets/Apollo.csv"
kims_path   = r"C:/Users/PAVAN KUMAR REDDY/Desktop/Revature Training/week-4/spark/datasets/KIMS.csv"

apollo = spark.read.csv(apollo_path, header=True, inferSchema=True)
kims   = spark.read.csv(kims_path, header=True, inferSchema=True)

apollo.createOrReplaceTempView("apollo")
kims.createOrReplaceTempView("kims")

print(" Apollo & KIMS datasets loaded successfully!\n")


# 4. DEFINE INSIGHT SCHEMA

schema = StructType([
    StructField("Insight", StringType(), True),
    StructField("Apollo_Value", StringType(), True),
    StructField("KIMS_Value", StringType(), True),
    StructField("Conclusion", StringType(), True)
])

insights = spark.createDataFrame([], schema)


#   INSIGHT 1: Patient Volume

pc = spark.sql("""
    SELECT 
        (SELECT COUNT(*) FROM apollo) AS Apollo_Count,
        (SELECT COUNT(*) FROM kims) AS KIMS_Count
""").collect()[0]

percentage_diff = round(((pc.KIMS_Count - pc.Apollo_Count) / pc.Apollo_Count) * 100, 2)

insights = insights.union(spark.createDataFrame([
    ("Patient Volume",
     str(pc.Apollo_Count), str(pc.KIMS_Count),
     f"KIMS handles {percentage_diff}% more patients than Apollo")
], schema))


#   INSIGHT 2: Dermatology Readmissions

derm = spark.sql("""
    SELECT
        (SELECT COUNT(*) FROM apollo 
         WHERE Department='Dermatology' AND Outcome='Readmitted') AS Apollo_Readm,

        (SELECT COUNT(*) FROM kims 
         WHERE Department='Dermatology' AND Outcome='Readmitted') AS KIMS_Readm
""").collect()[0]

insights = insights.union(spark.createDataFrame([
    ("Dermatology Readmissions",
     str(derm.Apollo_Readm), str(derm.KIMS_Readm),
     "Dermatology is the only department where Apollo has higher readmissions")
], schema))


#   INSIGHT 3: Cost Variance
var = spark.sql("""
    SELECT
        (SELECT VARIANCE(Treatment_Cost) FROM apollo) AS Apollo_Var,
        (SELECT VARIANCE(Treatment_Cost) FROM kims) AS KIMS_Var
""").collect()[0]

stable = "KIMS" if var.KIMS_Var < var.Apollo_Var else "Apollo"

insights = insights.union(spark.createDataFrame([
    ("Cost Variance",
     str(var.Apollo_Var), str(var.KIMS_Var),
     f"{stable} has a more stable cost distribution")
], schema))


#   INSIGHT 4 & 5: Min & Max Treatment Costs
mm = spark.sql("""
    SELECT
        (SELECT MIN(Treatment_Cost) FROM apollo) AS Ap_Min,
        (SELECT MAX(Treatment_Cost) FROM apollo) AS Ap_Max,
        (SELECT MIN(Treatment_Cost) FROM kims) AS K_Min,
        (SELECT MAX(Treatment_Cost) FROM kims) AS K_Max
""").collect()[0]

insights = insights.union(spark.createDataFrame([
    ("Apollo Min Cost", str(mm.Ap_Min), "", ""),
    ("Apollo Max Cost", str(mm.Ap_Max), "", ""),
    ("KIMS Min Cost", "", str(mm.K_Min), ""),
    ("KIMS Max Cost", "", str(mm.K_Max), "")
], schema))


#   INSIGHT 6: Discharge Rates
dr = spark.sql("""
    SELECT
        (SELECT ROUND((COUNT(*) * 100.0) / (SELECT COUNT(*) FROM apollo), 2)
         FROM apollo WHERE Outcome='Discharged') AS Apollo_Rate,

        (SELECT ROUND((COUNT(*) * 100.0) / (SELECT COUNT(*) FROM kims), 2)
         FROM kims WHERE Outcome='Discharged') AS KIMS_Rate
""").collect()[0]

insights = insights.union(spark.createDataFrame([
    ("Discharge Rate (%)",
     str(dr.Apollo_Rate), str(dr.KIMS_Rate),
     "KIMS shows better overall recovery efficiency")
], schema))


#   INSIGHT 7: High-Cost Treatments
high_cost = spark.sql("""
    SELECT
        (SELECT COUNT(*) FROM apollo WHERE Treatment_Cost > 100000) AS Ap_High,
        (SELECT COUNT(*) FROM kims WHERE Treatment_Cost > 100000) AS K_High
""").collect()[0]

conclusion = (
    "KIMS handles more high-cost (complex) cases"
    if high_cost.K_High > high_cost.Ap_High
    else "Apollo handles more high-cost (complex) cases"
)

insights = insights.union(spark.createDataFrame([
    ("High-Cost Treatments (>1 Lakh)",
     str(high_cost.Ap_High), str(high_cost.K_High), conclusion)
], schema))


#  6. SAVE INSIGHTS TO CSV

output_folder = "Hospital_Insights"
os.makedirs(output_folder, exist_ok=True)

csv_path = os.path.join(output_folder, "insights.csv")

insights_pdf = insights.toPandas()
insights_pdf.to_csv(csv_path, index=False)

print(f"\n All insights saved to: {csv_path}\n")

#  7. DISPLAY RESULTS

from tabulate import tabulate
import pandas as pd

df = pd.read_csv("Hospital_Insights/insights.csv")

print("\n=========== INSIGHTS TABLE ===========\n")
print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
print("\n=======================================\n")

