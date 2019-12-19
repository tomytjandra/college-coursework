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
    public partial class ChangePasswordForm : Form
    {
        private MainForm mainForm;
        private LoginController loginController;
        private RegisterController registerController;
        private string currentUsername;

        public ChangePasswordForm()
        {
            InitializeComponent();
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            string errMsg = "";
            string oldPassword = txtOldPassword.Text;
            string password = txtNewPassword.Text;
            string confirmPassword = txtConfirmPassword.Text;

            if (oldPassword == "" || password == "" || confirmPassword == "")
            {
                errMsg = "All field must be filled";
            }
            else if (!loginController.isUserRegistered(currentUsername, oldPassword))
            {
                errMsg = "Password is incorrect";
            }
            else if (password.Length < 3 || password.Length > 30)
            {
                errMsg = "Length of new password must be between 3 and 30 characters";
            }
            else if (password != confirmPassword)
            {
                errMsg = "Confirm password does not match with password";
            }
            else
            {
                registerController.changePassword(currentUsername, password);
                MessageBox.Show(this, "Change Password Success", "Change Password", MessageBoxButtons.OK, MessageBoxIcon.Information);
                this.Close();
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Change Password", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }

        private void ChangePasswordForm_Load(object sender, EventArgs e)
        {
            mainForm = (MainForm) this.MdiParent;
            loginController = new LoginController();
            registerController = new RegisterController();
            currentUsername = mainForm.getCurrentUser().userName;
        }

        private void txtOldPassword_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                btnSave_Click(this, new EventArgs());
            }
        }
    }
}
