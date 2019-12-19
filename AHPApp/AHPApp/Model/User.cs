using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AHPApp
{
    public class User
    {
        public int userId { get; set; }
        public string userName { get; set; }
        public string userPassword { get; set; }
        public bool isAdmin { get; set; }

        public User(string userName, bool isAdmin)
        {
            this.userName = userName;
            this.isAdmin = isAdmin;
        }
    }
}
