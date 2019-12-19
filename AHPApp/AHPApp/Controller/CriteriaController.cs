using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SQLite;
using System.Data;

namespace AHPApp
{
    class CriteriaController
    {
        static MainController mainController = new MainController();
        SQLiteConnection conn;
        SQLiteCommand cmd;
        SQLiteDataReader reader;

        public CriteriaController()
        {
            conn = mainController.getConnection();
            cmd = conn.CreateCommand();
        }

        public DataView getCriteriaData(string topicId)
        {
            conn.Open();

            DataSet ds = new DataSet();

            string query = "SELECT * FROM Criteria WHERE TopicId = " + topicId;
            SQLiteDataAdapter adapter = new SQLiteDataAdapter(query, conn);
            adapter.Fill(ds);

            conn.Close();

            return ds.Tables[0].DefaultView;
        }

        public bool isCriteriaUnique(string topicId, string criteriaName)
        {
            bool isUnique = true;
            conn.Open();

            cmd.CommandText =
                "SELECT * FROM Criteria WHERE TopicId = " + topicId + " AND " +
                "UPPER(CriteriaName) = '" + criteriaName.Replace("'", "''").ToUpper() + "'";
            reader = cmd.ExecuteReader();

            if (reader.Read())
            {
                isUnique = false;
            }

            reader.Close();
            conn.Close();
            return isUnique;
        }

        public List<Criteria> getCriteriaList(string topicId)
        {
            List<Criteria> listCriteria = new List<Criteria>();

            conn.Open();

            cmd.CommandText = "SELECT * FROM Criteria WHERE TopicId = " + topicId;
            reader = cmd.ExecuteReader();

            while (reader.Read())
            {
                Criteria criteria = new Criteria();
                criteria.criteriaId = Convert.ToInt32(reader.GetValue(0));
                criteria.criteriaName = Convert.ToString(reader.GetValue(2));
                criteria.criteriaUnit = Convert.ToString(reader.GetValue(3));
                criteria.isFewerBetter = Convert.ToBoolean(reader.GetValue(4));
                criteria.isBoolean = Convert.ToBoolean(reader.GetValue(5));
                listCriteria.Add(criteria);
            }

            reader.Close();
            conn.Close();
            return listCriteria;
        }

        public int addCriteria(string topicId, string criteriaName, string criteriaUnit, bool isFewerBetter, bool isBoolean, string userName)
        {
            conn.Open();

            cmd.CommandText =
                "INSERT INTO Criteria(TopicId, CriteriaName, CriteriaUnit, IsFewerBetter, IsBoolean, CreatedDate, CreatedBy) VALUES(" +
                topicId + ", " +
                "'" + criteriaName.Replace("'", "''") + "', " +
                "'" + criteriaUnit.Replace("'", "''") + "', " +
                "'" + isFewerBetter.ToString() + "', " +
                "'" + isBoolean.ToString() + "'," +
                "DATETIME()," +
                "'" + userName + "'" +
                ")";
            cmd.ExecuteNonQuery();

            int criteriaId = 0;
            cmd.CommandText = "SELECT last_insert_rowid()";
            reader = cmd.ExecuteReader();

            if (reader.Read())
            {
                criteriaId = reader.GetInt32(0);
            }

            reader.Close();
            conn.Close();
            return criteriaId;
        }

        public void editCriteria(string criteriaId, string criteriaName, string criteriaUnit, bool isFewerBetter, bool isBoolean, string userName)
        {
            conn.Open();

            cmd.CommandText =
                "UPDATE Criteria SET " +
                "CriteriaName = '" + criteriaName.Replace("'", "''") + "', " +
                "CriteriaUnit = '" + criteriaUnit.Replace("'", "''") + "', " +
                "IsFewerBetter = " + isFewerBetter.ToString() + ", " +
                "IsBoolean = " + isBoolean.ToString() + ", " +
                "LastModifiedDate = DATETIME(), " +
                "LastModifiedBy = '" + userName + "'" +
                "WHERE CriteriaId = " + criteriaId;
            cmd.ExecuteNonQuery();

            conn.Close();
        }

        public void deleteCriteria(string criteriaId)
        {
            conn.Open();

            cmd.CommandText = "DELETE FROM Criteria WHERE CriteriaId = " + criteriaId;
            cmd.ExecuteNonQuery();

            // on cascade manual
            cmd.CommandText = "DELETE FROM CriteriaWeight WHERE Criteria1Id = " + criteriaId + " OR Criteria2Id = " + criteriaId;
            cmd.ExecuteNonQuery();

            conn.Close();
        }

        public bool checkIsCriteriaWeightExist(string criteria1Id, string criteria2Id)
        {
            bool isExist = false;

            conn.Open();

            cmd.CommandText = "SELECT * FROM CriteriaWeight WHERE " +
                "Criteria1Id = " + criteria1Id + " AND Criteria2Id = " + criteria2Id;
            reader = cmd.ExecuteReader();

            if (reader.Read())
            {
                isExist = true;
            }

            reader.Close();
            conn.Close();
            return isExist;
        }

        public void autoInsertCriteriaWeight(string topicId)
        {
            CriteriaWeightController criteriaWeightController = new CriteriaWeightController();
            List<List<Criteria>> criteriaPairsList = criteriaWeightController.generateCriteriaPair(topicId);

            for (int i = 0; i < criteriaPairsList.Count; i++)
            {
                string criteria1Id = criteriaPairsList.ElementAt(i).ElementAt(0).criteriaId.ToString();
                string criteria2Id = criteriaPairsList.ElementAt(i).ElementAt(1).criteriaId.ToString();

                if (!checkIsCriteriaWeightExist(criteria1Id, criteria2Id))
                {
                    conn.Open();
                    cmd.CommandText =
                    "INSERT INTO CriteriaWeight(Criteria1Id, Criteria2Id) " +
                    "VALUES (" + criteria1Id + "," + criteria2Id + ")";
                    cmd.ExecuteNonQuery();
                    conn.Close();
                }
            }
        }
    }
}
