using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data;
using System.Data.SQLite;

namespace AHPApp
{
    class ViewUserController
    {
        static MainController mainController = new MainController();
        SQLiteConnection conn;
        SQLiteCommand cmd;
        SQLiteDataReader reader;

        public ViewUserController()
        {
            conn = mainController.getConnection();
            cmd = conn.CreateCommand();
        }

        public DataView getUserDataView(string currentUserName)
        {
            conn.Open();

            DataSet ds = new DataSet();

            string query = "SELECT UserId, UserName, IsAdmin, RegisteredDate FROM User WHERE UserName IS NOT '" + currentUserName + "'";

            SQLiteDataAdapter adapter = new SQLiteDataAdapter(query, conn);
            adapter.Fill(ds);

            conn.Close();

            return ds.Tables[0].DefaultView;
        }

        public void changeUserRole(string userId, bool isAdmin)
        {
            conn.Open();

            cmd.CommandText = "UPDATE User SET IsAdmin = '" + isAdmin.ToString().ToUpper() + "' WHERE UserId = " + userId;
            cmd.ExecuteNonQuery();

            conn.Close();
        }

        public void deleteUser(string userId)
        {
            conn.Open();

            cmd.CommandText = "DELETE FROM User WHERE UserId = " + userId;
            cmd.ExecuteNonQuery();

            conn.Close();
        }
    }
}
