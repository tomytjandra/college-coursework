using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SQLite;

namespace AHPApp
{
    public class RegisterController
    {
        static MainController mainController = new MainController();
        SQLiteConnection conn;
        SQLiteCommand cmd;
        SQLiteDataReader reader;

        public RegisterController()
        {
            conn = mainController.getConnection();
            cmd = conn.CreateCommand();
        }

        public void addUser(string username, string password)
        {
            string encryptedPassword = Encryptor.EncryptString(password, username);
            conn.Open();

            cmd.CommandText = "INSERT INTO User(UserName, UserPassword, RegisteredDate) VALUES ('" + username.Replace("'", "''") + "','" + encryptedPassword + "', DATETIME())";
            cmd.ExecuteNonQuery();

            conn.Close();
        }

        public bool isUsernameExist(string username)
        {
            bool isExist = false;

            conn.Open();
            cmd.CommandText = "SELECT * FROM User WHERE UPPER(UserName) = '" + username.ToUpper() + "'";
            reader = cmd.ExecuteReader();

            if (reader.Read())
            {
                isExist = true;
            }

            reader.Close();
            conn.Close();
            return isExist;
        }

        public void changePassword(string username, string newPassword)
        {
            string encryptedPassword = Encryptor.EncryptString(newPassword, username);
            conn.Open();

            cmd.CommandText = "UPDATE User SET UserPassword = '" + encryptedPassword + "' WHERE UserName = '" + username.Replace("'", "''") + "'";
            cmd.ExecuteNonQuery();

            conn.Close();
        }
    }
}
