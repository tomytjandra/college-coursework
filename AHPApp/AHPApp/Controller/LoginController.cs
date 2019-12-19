using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SQLite;

namespace AHPApp
{
    class LoginController
    {
        static MainController mainController = new MainController();
        SQLiteConnection conn;
        SQLiteCommand cmd;
        SQLiteDataReader reader;

        public LoginController()
        {
            conn = mainController.getConnection();
            cmd = conn.CreateCommand();
        }

        public bool isUserRegistered(string username, string password)
        {
            bool isRegistered = false;
            string encryptedPassword = Encryptor.EncryptString(password, username);

            conn.Open();

            cmd.CommandText = "SELECT * FROM User WHERE " +
                "UserName = '" + username.Replace("'", "''") + "' AND " +
                "UserPassword = '" + encryptedPassword + "'";
            reader = cmd.ExecuteReader();

            if (reader.Read())
            {
                isRegistered = true;
            }

            reader.Close();
            conn.Close();
            return isRegistered;
        }

        public bool isAdmin(string username)
        {
            bool isAdmin = false;

            conn.Open();
            cmd.CommandText = "SELECT IsAdmin FROM User WHERE " +
                "UserName = '" + username.Replace("'", "''") + "'";
            reader = cmd.ExecuteReader();

            if (reader.Read())
            {
                isAdmin = (bool) reader.GetValue(0);
            }

            reader.Close();
            conn.Close();
            return isAdmin;
        }

        public void addSession(string username)
        {
            conn.Open();

            cmd.CommandText = "INSERT INTO Session(UserName) VALUES ('" + username.Replace("'", "''") + "')";
            cmd.ExecuteNonQuery();

            conn.Close();
        }
    }
}
