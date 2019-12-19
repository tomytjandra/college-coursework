using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data;
using System.Data.SQLite;

namespace AHPApp
{
    class AlternativeListController
    {
        static MainController mainController = new MainController();
        SQLiteConnection conn;
        SQLiteCommand cmd;
        SQLiteDataReader reader;

        public AlternativeListController()
        {
            conn = mainController.getConnection();
            cmd = conn.CreateCommand();
        }

        public List<string> getCreatedDetail4OneRow(List<int> detailIdList)
        {
            List<string> createdDetail = new List<string>();
            string createdDate = "";
            string createdBy = "";

            string detailIdListString = "";
            for (int i = 0; i < detailIdList.Count; i++)
            {
                if (i == detailIdList.Count - 1)
                {
                    detailIdListString += detailIdList.ElementAt(i).ToString();
                }
                else
                {
                    detailIdListString += detailIdList.ElementAt(i).ToString() + ",";
                }
            }

            conn.Open();

            cmd.CommandText = "SELECT MAX(CreatedDate), CreatedBy FROM DetailAlternative WHERE DetailId IN (" + detailIdListString + ") AND CreatedDate IS NOT NULL GROUP BY CreatedBy";
            reader = cmd.ExecuteReader();

            if (reader.Read())
            {
                createdDate = reader.GetString(0);
                createdBy = reader.GetString(1);
            }

            reader.Close();
            conn.Close();

            createdDetail.Add(createdDate);
            createdDetail.Add(createdBy);
            return createdDetail;
        }

        public List<string> getLastModifiedDetail4OneRow(List<int> detailIdList)
        {
            List<string> lastModifiedDetail = new List<string>();
            string lastModifiedDate = "";
            string lastModifiedBy = "";

            string detailIdListString = "";
            for (int i = 0; i < detailIdList.Count; i++)
            {
                if (i == detailIdList.Count - 1)
                {
                    detailIdListString += detailIdList.ElementAt(i).ToString();
                }
                else
                {
                    detailIdListString += detailIdList.ElementAt(i).ToString() + ",";
                }
            }

            conn.Open();

            cmd.CommandText = "SELECT MAX(LastModifiedDate), LastModifiedBy FROM DetailAlternative WHERE DetailId IN (" + detailIdListString + ") GROUP BY LastModifiedBy";
            reader = cmd.ExecuteReader();

            if (reader.Read())
            {
                if (!reader.IsDBNull(0))
                {
                    lastModifiedDate = reader.GetString(0);
                    lastModifiedBy = reader.GetString(1);
                }
            }

            reader.Close();
            conn.Close();

            lastModifiedDetail.Add(lastModifiedDate);
            lastModifiedDetail.Add(lastModifiedBy);
            return lastModifiedDetail;
        }

        public DataTable getDetailDataTable(string topicId)
        {
            conn.Open();

            DataSet ds = new DataSet();

            string query = "SELECT * FROM DetailAlternative, Criteria WHERE " +
                "Criteria.CriteriaId = DetailAlternative.CriteriaId AND " +
                "Criteria.TopicId = " + topicId;
            SQLiteDataAdapter adapter = new SQLiteDataAdapter(query, conn);
            adapter.Fill(ds);

            conn.Close();

            return ds.Tables[0];
        }

        public List<DetailAlternative> getDetailList(string topicId)
        {
            List<DetailAlternative> detailAlternativeList = new List<DetailAlternative>();

            conn.Open();

            cmd.CommandText = "SELECT DetailId, Criteria.CriteriaId, AlternativeName, Value, DetailAlternative.CreatedDate, DetailAlternative.CreatedBy, DetailAlternative.LastModifiedDate, DetailAlternative.LastModifiedBy FROM DetailAlternative, Criteria WHERE " +
                "Criteria.CriteriaId = DetailAlternative.CriteriaId AND " +
                "Criteria.TopicId = " + topicId;
            reader = cmd.ExecuteReader();

            while (reader.Read())
            {
                DetailAlternative detailAlternative = new DetailAlternative();
                detailAlternative.detailId = reader.GetInt32(0);
                detailAlternative.criteriaId = reader.GetInt32(1);
                detailAlternative.alternativeName = reader.GetString(2);
                detailAlternative.value = reader.GetDouble(3);
                detailAlternativeList.Add(detailAlternative);
            }

            reader.Close();
            conn.Close();

            return detailAlternativeList;
        }

        public List<DetailAlternative> getDetailListPerCriteria(string topicId, string criteriaId)
        {
            List<DetailAlternative> detailAlternativeList = new List<DetailAlternative>();

            conn.Open();

            cmd.CommandText = "SELECT DetailId, Criteria.CriteriaId, AlternativeName, Value, DetailAlternative.CreatedDate, DetailAlternative.CreatedBy, DetailAlternative.LastModifiedDate, DetailAlternative.LastModifiedBy FROM DetailAlternative, Criteria WHERE " +
                "Criteria.CriteriaId = DetailAlternative.CriteriaId AND " +
                "Criteria.TopicId = " + topicId + " AND Criteria.CriteriaId = " + criteriaId;
            reader = cmd.ExecuteReader();

            while (reader.Read())
            {
                DetailAlternative detailAlternative = new DetailAlternative();
                //detailAlternative.detailId = reader.GetInt32(0);
                //detailAlternative.criteriaId = reader.GetInt32(1);
                detailAlternative.alternativeName = reader.GetString(2);
                detailAlternative.value = reader.GetDouble(3);
                detailAlternativeList.Add(detailAlternative);
            }

            reader.Close();
            conn.Close();

            return detailAlternativeList;
        }

        public List<string> getAlternativeList(string topicId)
        {
            DataTable dt = getDetailDataTable(topicId);

            // Convert DataTable to List
            List<string> altList = new List<string>();
            foreach (DataRow row in dt.Rows)
            {
                altList.Add(Convert.ToString(row["AlternativeName"]));
            }

            return altList.Distinct().ToList();
        }

        public int countCertainAlternativeName(string topicId, string alternativeName)
        {
            int count = 0;

            List<string> alternativeNameList = getAlternativeList(topicId);

            foreach(string alt in alternativeNameList)
            {
                if (alt.ToUpper() == alternativeName.ToUpper())
                {
                    count++;
                }
            }

            return count;
        }

        public double valueLookup(int criteriaId, string altName)
        {
            conn.Open();

            cmd = conn.CreateCommand();

            cmd.CommandText = "SELECT Value FROM DetailAlternative WHERE AlternativeName = '" + altName + "' AND CriteriaId = " + criteriaId;
            reader = cmd.ExecuteReader();

            double value = 0;
            if (reader.Read())
            {
                value = reader.GetDouble(0);
            }

            reader.Close();
            conn.Close();
            return value;
        }

        public bool isDetailAlternativeExist(int criteriaId, string alternativeName)
        {
            bool isExist = false;

            conn.Open();

            cmd = conn.CreateCommand();

            cmd.CommandText =
                "SELECT * FROM DetailAlternative " +
                "WHERE CriteriaId = "+ criteriaId +" AND AlternativeName = '"+ alternativeName +"'";
            reader = cmd.ExecuteReader();
            
            if (reader.Read())
            {
                isExist = true;
            }

            reader.Close();
            conn.Close();
            return isExist;
        }

        public void addOneDetailAlternative(int criteriaId, string alternativeName, double value, string userName)
        {
            conn.Open();

            cmd = conn.CreateCommand();

            cmd.CommandText =
                "INSERT INTO DetailAlternative(CriteriaId, AlternativeName, Value, CreatedDate, CreatedBy) " +
                "VALUES("+ criteriaId +", '"+ alternativeName +"', "+ value +", DATETIME(), '" + userName + "')";
            cmd.ExecuteNonQuery();

            conn.Close();
        }

        public void editOneDetailAlternative(int criteriaId, string oldAlternativeName, string newAlternativeName, double value, string userName)
        {
            bool isExist = isDetailAlternativeExist(criteriaId, oldAlternativeName);

            conn.Open();

            cmd = conn.CreateCommand();

            if (!isExist)
            {
                cmd.CommandText = "INSERT INTO DetailAlternative(CriteriaId, AlternativeName, Value, CreatedDate, CreatedBy) " +
                    "VALUES(" + criteriaId + ",'" + oldAlternativeName + "', 0, DATETIME(), '" + userName + "')";
                cmd.ExecuteNonQuery();
            }
            

            cmd.CommandText =
                "UPDATE DetailAlternative " +
                "SET AlternativeName = '" + newAlternativeName + "'," +
                "Value = " + value + "," +
                "LastModifiedDate = DATETIME(), "+
                "LastModifiedBy = '" + userName + "'" +
                "WHERE CriteriaId = "+ criteriaId +" AND AlternativeName = '"+ oldAlternativeName +"'";
            cmd.ExecuteNonQuery();

            conn.Close();
        }

        public void deleteOneDetailAlternative(int detailId)
        {
            conn.Open();

            cmd = conn.CreateCommand();

            cmd.CommandText =
                "DELETE FROM DetailAlternative WHERE DetailId = " + detailId.ToString();
            cmd.ExecuteNonQuery();

            conn.Close();
        }

        public void deleteAllDetailAlternativePerCriteria(string criteriaId)
        {
            conn.Open();

            cmd = conn.CreateCommand();

            cmd.CommandText =
                "DELETE FROM DetailAlternative WHERE CriteriaId = " + criteriaId.ToString();
            cmd.ExecuteNonQuery();

            conn.Close();
        }

        public int lookupDetailId(string alternativeName, int criteriaId)
        {
            int detailId = -1;

            conn.Open();

            cmd = conn.CreateCommand();

            cmd.CommandText =
                "SELECT * FROM DetailAlternative " +
                "WHERE CriteriaId = " + criteriaId + " AND AlternativeName = '" + alternativeName + "'";
            reader = cmd.ExecuteReader();

            if (reader.Read())
            {
                detailId = reader.GetInt32(0);
            }

            reader.Close();
            conn.Close();
            return detailId;
        }

        public void updateLastModified(int detailId, string userName)
        {
            conn.Open();

            cmd = conn.CreateCommand();

            cmd.CommandText =
                "UPDATE DetailAlternative " +
                "SET LastModifiedDate = DATETIME()," +
                "LastModifiedBy = '" + userName + "'" +
                "WHERE DetailId = " + detailId;
            cmd.ExecuteNonQuery();

            conn.Close();
        }

        public void fromNotBoolean2Boolean(string criteriaId)
        {
            conn.Open();

            cmd = conn.CreateCommand();

            cmd.CommandText =
                "UPDATE DetailAlternative SET Value = 1 WHERE DetailId IN (" +
                "SELECT DetailId FROM DetailAlternative WHERE CriteriaId = " + criteriaId + " AND Value > 0" +
                ")";
            cmd.ExecuteNonQuery();

            conn.Close();
        }

        public void fromBoolean2NotBoolean(string criteriaId)
        {
            conn.Open();

            cmd = conn.CreateCommand();

            cmd.CommandText =
                "UPDATE DetailAlternative SET Value = 0 WHERE CriteriaId = " + criteriaId;
            cmd.ExecuteNonQuery();

            conn.Close();
        }
    }
}
