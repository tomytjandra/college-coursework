using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SQLite;
using System.Data;

namespace AHPApp
{
    class TopicController
    {
        static MainController mainController = new MainController();
        SQLiteConnection conn;
        SQLiteCommand cmd;
        SQLiteDataReader reader;

        public TopicController()
        {
            conn = mainController.getConnection();
            cmd = conn.CreateCommand();
        }

        public DataView getTopicData(string userName)
        {
            conn.Open();

            DataSet ds = new DataSet();

            string query = "";
            if (userName == "")
            {
                query = "SELECT * FROM Topic";
            }
            else
            {
                query = "SELECT * FROM Topic WHERE CreatedBy = '" + userName + "'";
            }
            
            SQLiteDataAdapter adapter = new SQLiteDataAdapter(query, conn);
            adapter.Fill(ds);

            conn.Close();

            return ds.Tables[0].DefaultView;
        }

        public bool isTopicUnique(string topicName)
        {
            bool isUnique = true;
            conn.Open();

            cmd.CommandText = "SELECT * FROM Topic WHERE UPPER(TopicName) = '" + topicName.Replace("'","''").ToUpper() + "'";
            reader = cmd.ExecuteReader();

            if (reader.Read())
            {
                isUnique = false;
            }

            reader.Close();
            conn.Close();
            return isUnique;
        }

        public void addTopic(string topicName, string userName)
        {
            conn.Open();

            cmd.CommandText = "INSERT INTO Topic(TopicName, CreatedDate, CreatedBy) VALUES('" + topicName.Replace("'", "''") + "', DATETIME(), '" + userName + "')";
            cmd.ExecuteNonQuery();

            conn.Close();
        }

        public void editTopic(string topicId, string topicName, string userName)
        {
            conn.Open();

            cmd.CommandText = "UPDATE Topic SET TopicName = '" + topicName.Replace("'", "''") + "', LastModifiedDate = DATETIME(), LastModifiedBy = '" + userName + "' WHERE TopicId = " + topicId;
            cmd.ExecuteNonQuery();

            conn.Close();
        }

        public void deleteTopic(string topicId)
        {
            conn.Open();

            cmd.CommandText = "DELETE FROM Topic WHERE TopicId = " + topicId;
            cmd.ExecuteNonQuery();

            // on cascade manual
            cmd.CommandText = "DELETE FROM Criteria WHERE TopicId = " + topicId;
            cmd.ExecuteNonQuery();

            conn.Close();
        }
    }
}