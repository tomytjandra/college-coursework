using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SQLite;
using System.Data;

namespace AHPApp
{
    class CriteriaWeightController
    {
        static MainController mainController = new MainController();
        SQLiteConnection conn;
        SQLiteCommand cmd;
        SQLiteDataReader reader;

        public CriteriaWeightController()
        {
            conn = mainController.getConnection();
            cmd = conn.CreateCommand();
        }

        public DataTable getCriteriaWeightDataTable(string topicId)
        {
            conn.Open();

            DataSet ds = new DataSet();

            string query =
                "SELECT Table1.CriteriaWeightId, Table1.CriteriaId AS Criteria1Id, Table2.CriteriaId AS Criteria2Id, Table1.CriteriaName AS Criteria1Name, Table2.CriteriaName AS Criteria2Name, Table1.ImportanceLevel " +
                "FROM " +
                "Topic, Criteria, " +
                "(SELECT * FROM Criteria, CriteriaWeight WHERE Criteria.CriteriaId = CriteriaWeight.Criteria1Id) AS Table1, " +
                "(SELECT * FROM Criteria, CriteriaWeight WHERE Criteria.CriteriaId = CriteriaWeight.Criteria2Id) AS Table2 " +
                "WHERE Topic.TopicId = Criteria.TopicId AND Criteria.CriteriaId = Table1.CriteriaId AND Table1.CriteriaWeightId = Table2.CriteriaWeightId AND " +
                "Topic.TopicId = " + topicId;
            SQLiteDataAdapter adapter = new SQLiteDataAdapter(query, conn);
            adapter.Fill(ds);

            conn.Close();

            return ds.Tables[0];
        }

        public List<CriteriaWeight> getCriteriaWeightListName(string topicId)
        {
            DataTable dt = getCriteriaWeightDataTable(topicId);

            // Convert DataTable to List
            List<CriteriaWeight> criteriaWeightList = new List<CriteriaWeight>();
            foreach (DataRow row in dt.Rows)
            {
                criteriaWeightList.Add(new CriteriaWeight
                {
                    criteriaWeightId = Convert.ToInt32(row["CriteriaWeightId"]),
                    criteria1Id = Convert.ToInt32(row["Criteria1Id"]),
                    criteria2Id = Convert.ToInt32(row["Criteria2Id"]),
                    criteria1Name = Convert.ToString(row["Criteria1Name"]),
                    criteria2Name = Convert.ToString(row["Criteria2Name"]),
                    importanceLevel = Convert.ToDouble(row["ImportanceLevel"])
                });
            }

            return criteriaWeightList;
        }

        public DataTable getCriteriaDataTable(string topicId)
        {
            conn.Open();

            DataSet ds = new DataSet();

            string query = "SELECT CriteriaId, CriteriaName FROM Criteria WHERE TopicId = " + topicId;
            SQLiteDataAdapter adapter = new SQLiteDataAdapter(query, conn);
            adapter.Fill(ds);

            conn.Close();

            return ds.Tables[0];
        }

        public List<List<Criteria>> generateCriteriaPair(string topicId)
        {
            DataTable dt = getCriteriaDataTable(topicId);

            // Convert DataTable to List
            List<Criteria> criteriaList = new List<Criteria>();
            foreach (DataRow row in dt.Rows)
            {
                criteriaList.Add(new Criteria {
                    criteriaId = Convert.ToInt32(row["CriteriaId"]),
                    criteriaName = Convert.ToString(row["CriteriaName"])
                });
            }

            // [[criteria1, criteria2], [criteria1, criteria2], [criteria1, criteria2]]
            List<List<Criteria>> criteriaPairsList = new List<List<Criteria>>();
            for (int i = 0; i < criteriaList.Count - 1; i++)
            {
                for (int j = i + 1; j < criteriaList.Count; j++)
                {
                    List<Criteria> criteriaPair = new List<Criteria>();
                    criteriaPair.Add(criteriaList.ElementAt(i));
                    criteriaPair.Add(criteriaList.ElementAt(j));
                    criteriaPairsList.Add(criteriaPair);
                }
            }
            return criteriaPairsList;
        }

        public List<double> getImportanceLevelList(string topicId)
        {
            DataTable dt = getCriteriaWeightDataTable(topicId);

            // Convert DataTable to List
            List<double> importanceLevelList = new List<double>();
            foreach (DataRow row in dt.Rows)
            {
                importanceLevelList.Add(Convert.ToDouble(row["ImportanceLevel"]));
            }

            return importanceLevelList;
        }

        public void editOneCriteriaWeight(int criteriaWeightId, double importanceLevel)
        {
            conn.Open();

            cmd.CommandText =
                "UPDATE CriteriaWeight SET ImportanceLevel = " + importanceLevel.ToString() + " " +
                "WHERE CriteriaWeightId = " + criteriaWeightId.ToString();
            cmd.ExecuteNonQuery();

            conn.Close();
        }
    }
}
