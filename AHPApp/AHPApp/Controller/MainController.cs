using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SQLite;

namespace AHPApp
{
    class MainController
    {
        SQLiteConnection conn;
        SQLiteCommand cmd;
        SQLiteDataReader reader;

        public MainController()
        {
            connectDatabase();
            initializeNewDatabase();
        }

        public SQLiteConnection getConnection()
        {
            return this.conn;
        }

        public void connectDatabase()
        {
            string databaseName = "dataAHPApp.db";
            string version = "3";
            string connectionDetail = "DataSource=" + databaseName + ";Version=" + version + ";New=True;Compress=True;";
            conn = new SQLiteConnection(connectionDetail);
        }

        public void dropAllTable()
        {
            conn.Open();

            cmd = conn.CreateCommand();

            cmd.CommandText =
                "DROP TABLE IF EXISTS Topic";
            cmd.ExecuteNonQuery();

            cmd.CommandText =
                "DROP TABLE IF EXISTS Alternative";
            cmd.ExecuteNonQuery();

            cmd.CommandText =
                "DROP TABLE IF EXISTS Criteria";
            cmd.ExecuteNonQuery();

            cmd.CommandText =
                "DROP TABLE IF EXISTS CriteriaWeight";
            cmd.ExecuteNonQuery();

            cmd.CommandText =
                "DROP TABLE IF EXISTS DetailAlternative";
            cmd.ExecuteNonQuery();

            conn.Close();
        }
        
        public void createDefaultAdmin()
        {
            cmd = conn.CreateCommand();
            cmd.CommandText = "INSERT INTO User(UserName, UserPassword, IsAdmin) VALUES(" +
                "'admin'" +
                Encryptor.EncryptString("admin", "admin") +
                "TRUE" +
                ")";
            cmd.ExecuteNonQuery();
        }

        public void initializeNewDatabase()
        {
            conn.Open();

            cmd = conn.CreateCommand();

            // Table Session
            //cmd.CommandText =
            //    "CREATE TABLE IF NOT EXISTS Session(" +
            //        "UserName VARCHAR(100) NOT NULL" +
            //    ")";
            //cmd.ExecuteNonQuery();

            // Table User
            cmd.CommandText =
                "CREATE TABLE IF NOT EXISTS User(" +
                    "UserId INTEGER PRIMARY KEY AUTOINCREMENT," +
                    "UserName VARCHAR(100) NOT NULL UNIQUE," +
                    "UserPassword VARCHAR(100) NOT NULL," +
                    "IsAdmin BIT DEFAULT 'FALSE'," +
                    "RegisteredDate TEXT" +
                ")";
            cmd.ExecuteNonQuery();

            try
            {
                cmd.CommandText = "INSERT INTO User(UserName, UserPassword, IsAdmin) VALUES(" +
                "'admin'," +
                "'" + Encryptor.EncryptString("admin", "admin") + "'," +
                "'TRUE'" +
                ")";
                cmd.ExecuteNonQuery();
            }
            catch
            {

            }

            // Table Topic
            cmd.CommandText =
                "CREATE TABLE IF NOT EXISTS Topic(" +
                    "TopicId INTEGER PRIMARY KEY AUTOINCREMENT," +
                    "TopicName VARCHAR(100) NOT NULL UNIQUE," +
                    "CreatedDate TEXT NOT NULL," +
                    "CreatedBy VARCHAR(100) NOT NULL," +
                    "LastModifiedDate TEXT," +
                    "LastModifiedBy VARCHAR(100)" +
                ")";
            cmd.ExecuteNonQuery();

            // Table Alternative
            //cmd.CommandText =
            //    "CREATE TABLE IF NOT EXISTS Alternative(" +
            //        "AlternativeId INTEGER PRIMARY KEY AUTOINCREMENT," +
            //        "AlternativeName VARCHAR(100) NOT NULL" +
            //    ")";
            //cmd.ExecuteNonQuery();

            // Table Criteria
            cmd.CommandText =
                "CREATE TABLE IF NOT EXISTS Criteria(" +
                    "CriteriaId INTEGER PRIMARY KEY AUTOINCREMENT," +
                    "TopicId INTEGER REFERENCES Topic(TopicId) ON DELETE CASCADE," +
                    "CriteriaName VARCHAR(100) NOT NULL," +
                    "CriteriaUnit VARCHAR(100)," +
                    "IsFewerBetter BIT DEFAULT 'FALSE'," +
                    "IsBoolean BIT DEFAULT 'FALSE'," +
                    "CreatedDate TEXT NOT NULL," +
                    "CreatedBy VARCHAR(100) NOT NULL," +
                    "LastModifiedDate TEXT," +
                    "LastModifiedBy VARCHAR(100)" +
                ")";
            cmd.ExecuteNonQuery();

            // Table CriteriaWeight
            cmd.CommandText =
                "CREATE TABLE IF NOT EXISTS CriteriaWeight(" +
                    "CriteriaWeightId INTEGER PRIMARY KEY AUTOINCREMENT," +
                    "Criteria1Id INTEGER REFERENCES Criteria(CriteriaId) ON DELETE CASCADE," +
                    "Criteria2Id INTEGER REFERENCES Criteria(CriteriaId) ON DELETE CASCADE," +
                    "ImportanceLevel DECIMAL DEFAULT 1" +
                ")";
            cmd.ExecuteNonQuery();

            // Table DetailAlternative
            cmd.CommandText =
                "CREATE TABLE IF NOT EXISTS DetailAlternative(" +
                    "DetailId INTEGER PRIMARY KEY AUTOINCREMENT," +
                    "AlternativeName VARCHAR(100) NOT NULL," +
                    "CriteriaId INTEGER REFERENCES Criteria(CriteriaId) ON DELETE CASCADE," +
                    "Value DECIMAL NOT NULL," +
                    "CreatedDate TEXT," +
                    "CreatedBy VARCHAR(100)," +
                    "LastModifiedDate TEXT," +
                    "LastModifiedBy VARCHAR(100)" +
                ")";
            cmd.ExecuteNonQuery();

            conn.Close();
        }

        public int countCriteria(string topicId)
        {
            int count = 0;
            conn.Open();

            cmd.CommandText = "SELECT COUNT(*) FROM Criteria WHERE TopicId = " + topicId;
            reader = cmd.ExecuteReader();

            if (reader.Read())
            {
                count = reader.GetInt32(0);
            }

            reader.Close();
            conn.Close();
            return count;
        }

        public bool isAllCriteriaWeightDefault(string topicId)
        {
            bool isDefault = true;
            conn.Open();

            cmd.CommandText =
                "SELECT ImportanceLevel FROM Topic, Criteria, CriteriaWeight WHERE " +
                "Topic.TopicId = Criteria.TopicId AND " +
                "(Criteria.CriteriaId = CriteriaWeight.Criteria1Id OR Criteria.CriteriaId = CriteriaWeight.Criteria2Id) AND " +
                "Topic.TopicId = " + topicId;
            reader = cmd.ExecuteReader();

            while (reader.Read())
            {
                double importanceLevel = reader.GetDouble(0);
                if (importanceLevel != 1)
                {
                    isDefault = false;
                    break;
                }
            }

            reader.Close();
            conn.Close();
            return isDefault;
        }

        public bool isDetailAlternativeExist(string topicId)
        {
            bool isExist = false;
            conn.Open();

            cmd.CommandText =
                "SELECT * FROM Topic, Criteria, DetailAlternative WHERE " +
                "Topic.TopicId = Criteria.TopicId AND " +
                "Criteria.CriteriaId = DetailAlternative.CriteriaId AND " +
                "Topic.TopicId = " + topicId;
            reader = cmd.ExecuteReader();

            if (reader.Read())
            {
                isExist = true;
            }

            reader.Close();
            conn.Close();
            return isExist;
        }

        public void addDummyData()
        {
            conn.Open();

            cmd.CommandText = "INSERT INTO Topic(TopicName) VALUES('GPU Comparison')";
            cmd.ExecuteNonQuery();

            cmd.CommandText = "INSERT INTO Topic(TopicName) VALUES('CPU Comparison')";
            cmd.ExecuteNonQuery();

            cmd.CommandText = "INSERT INTO Criteria(TopicId, CriteriaName, CriteriaUnit) VALUES(1, 'Memory GPU', 'MB')";
            cmd.ExecuteNonQuery();

            cmd.CommandText = "INSERT INTO Criteria(TopicId, CriteriaName, CriteriaUnit) VALUES(1, 'Bandwith', 'MB')";
            cmd.ExecuteNonQuery();

            cmd.CommandText = "INSERT INTO Criteria(TopicId, CriteriaName, CriteriaUnit, IsFewerBetter) VALUES(1, 'Price', 'Rupiah', True)";
            cmd.ExecuteNonQuery();

            cmd.CommandText = "INSERT INTO Criteria(TopicId, CriteriaName, CriteriaUnit) VALUES(2, 'Memory CPU', 'MB')";
            cmd.ExecuteNonQuery();

            cmd.CommandText = "INSERT INTO Alternative(AlternativeName) VALUES('GPU 1')";
            cmd.ExecuteNonQuery();

            cmd.CommandText = "INSERT INTO DetailAlternative(AlternativeId, CriteriaId, Value) VALUES(1, 1, 100)";
            cmd.ExecuteNonQuery();

            cmd.CommandText = "INSERT INTO DetailAlternative(AlternativeId, CriteriaId, Value) VALUES(1, 2, 200)";
            cmd.ExecuteNonQuery();

            conn.Close();
        }

        public void deleteSession()
        {
            conn.Open();

            cmd.CommandText = "DELETE FROM Session";
            cmd.ExecuteNonQuery();

            conn.Close();
        }

        public string checkSession()
        {
            string username = "";

            conn.Open();

            cmd.CommandText = "SELECT * FROM Session";
            reader = cmd.ExecuteReader();

            if (reader.Read())
            {
                username = reader.GetString(0);
            }

            reader.Close();
            conn.Close();
            return username;
        }
    }
}