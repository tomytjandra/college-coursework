using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Security.Cryptography;

namespace AHPApp
{
    public partial class RegisterForm : Form
    {
        private MainForm mainForm;
        RegisterController registerController;
        MD5 md5 = new MD5CryptoServiceProvider();
        private string action;
        private string selectedUserName;

        public RegisterForm(string action, string selectedUserName)
        {
            InitializeComponent();
            this.action = action;
            this.selectedUserName = selectedUserName;
        }

        public void resetForm()
        {
            txtUsername.Text = "";
            txtPassword.Text = "";
            txtConfirmPassword.Text = "";
        }

        private void btnRegister_Click(object sender, EventArgs e)
        {
            string errMsg = "";
            string username = txtUsername.Text;
            string password = txtPassword.Text;
            string confirmPassword = txtConfirmPassword.Text;

            if (username == "" || password == "" || confirmPassword == "")
            {
                errMsg = "All field must be filled";
            }
            else if (username.Length < 3 || username.Length > 30)
            {
                errMsg = "Length of username must be between 3 and 30 characters";
            }
            else if (registerController.isUsernameExist(username))
            {
                errMsg = "Someone has registered with the same username";
            }
            else if (password.Length < 3 || password.Length > 30)
            {
                errMsg = "Length of password must be between 3 and 30 characters";
            }
            else if (password != confirmPassword)
            {
                errMsg = "Confirm password does not match with password";
            }
            else
            {
                registerController.addUser(username, password);
                resetForm();
                MessageBox.Show(this, "Register Success", "Register", MessageBoxButtons.OK, MessageBoxIcon.Information);
                this.Close();
                mainForm.loginToolStripMenuItem1_Click(this, new EventArgs());
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Register", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }

        private void RegisterForm_Load(object sender, EventArgs e)
        {
            registerController = new RegisterController();
            mainForm = (MainForm)this.MdiParent;

            if (action == "Register")
            {
                lblResetPasswordUsername.Visible = false;
                txtUsername.Visible = true;
                btnRegister.Visible = true;
                btnResetPassword.Visible = false;
            }
            else if (action == "Reset Password")
            {
                this.Text = "Reset Password";
                lblUsername.Text = "Username";
                lblResetPasswordUsername.Text = selectedUserName;
                lblPassword.Text = "New Password *";

                lblResetPasswordUsername.Visible = true;
                txtUsername.Visible = false;
                btnRegister.Visible = false;
                btnResetPassword.Visible = true;
            }

        }

        private void txtUsername_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                if (action == "Register")
                {
                    btnRegister_Click(this, new EventArgs());
                }
                else if (action == "Reset Password")
                {
                    btnResetPassword_Click(this, new EventArgs());
                }
            }
        }

        private void btnResetPassword_Click(object sender, EventArgs e)
        {
            string errMsg = "";
            string password = txtPassword.Text;
            string confirmPassword = txtConfirmPassword.Text;

            if (password == "" || confirmPassword == "")
            {
                errMsg = "All field must be filled";
            }
            else if (password.Length < 3 || password.Length > 30)
            {
                errMsg = "Length of password must be between 3 and 30 characters";
            }
            else if (password != confirmPassword)
            {
                errMsg = "Confirm password does not match with password";
            }
            else
            {
                registerController.changePassword(selectedUserName, password);
                resetForm();
                MessageBox.Show(this, "Reset Password Success", "Reset Password", MessageBoxButtons.OK, MessageBoxIcon.Information);
                this.Close();
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Reset Password", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }
    }
}
