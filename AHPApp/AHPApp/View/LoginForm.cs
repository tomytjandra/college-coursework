using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace AHPApp
{
    public partial class LoginForm : Form
    {
        private MainForm mainForm;
        LoginController loginController;

        public LoginForm()
        {
            InitializeComponent();
        }

        private void btnLogin_Click(object sender, EventArgs e)
        {
            string errMsg = "";
            string username = txtUsername.Text;
            string password = txtPassword.Text;

            if (username == "" || password == "")
            {
                errMsg = "All field must be filled";
            }
            else if (!loginController.isUserRegistered(username, password))
            {
                errMsg = "Wrong username and password combination";
            }
            else
            {
                bool isAdmin = loginController.isAdmin(username);
                User currentUser = new User(username, isAdmin);
                mainForm.setCurrentUser(currentUser);
                MessageBox.Show(this, "Hi, " + username + "!\nYou've successfully logged in.", "Login", MessageBoxButtons.OK, MessageBoxIcon.Information);
                mainForm.updateTooltipVisibility();
                mainForm.closeAllChildrenFormExcept(null, null);
                //loginController.addSession(username);
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Login", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }

        private void LoginForm_Load(object sender, EventArgs e)
        {
            loginController = new LoginController();
            mainForm = (MainForm)this.MdiParent;
        }

        private void txtPassword_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                btnLogin_Click(this, new EventArgs());
            }
        }
    }
}
