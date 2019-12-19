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
    public partial class ViewUserForm : Form
    {
        private MainForm mainForm;
        private ViewUserController viewUserController;
        private User currentUser;
        private DataView data;

        public ViewUserForm()
        {
            InitializeComponent();
        }

        private void ViewUserForm_Load(object sender, EventArgs e)
        {
            mainForm = (MainForm)this.MdiParent;
            viewUserController = new ViewUserController();
            currentUser = mainForm.getCurrentUser();
            refreshForm();
        }

        private void refreshForm()
        {
            data = viewUserController.getUserDataView(currentUser.userName);
            dataGridView1.DataSource = data;
            dataGridView1.ClearSelection();
            dataGridView1.Columns[0].Visible = false;
        }

        private void btnDeleteUser_Click(object sender, EventArgs e)
        {
            string errMsg = "";

            if (dataGridView1.SelectedCells.Count == 0)
            {
                errMsg = "Select user to be deleted";
            }
            else
            {
                string selectedUserId = dataGridView1.SelectedCells[0].Value.ToString();
                string selectedUserName = dataGridView1.SelectedCells[1].Value.ToString();
                
                var mboxResponse = MessageBox.Show(this, "This action will delete the user \"" + selectedUserName + "\". Are you sure?", "Delete User: " + selectedUserName, MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                if (mboxResponse == DialogResult.Yes)
                {
                    viewUserController.deleteUser(selectedUserId);
                    refreshForm();
                    MessageBox.Show(this, "Delete Success", "Delete User", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Delete User", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }

        private void btnChangeRole_Click(object sender, EventArgs e)
        {
            string errMsg = "";

            if (dataGridView1.SelectedCells.Count == 0)
            {
                errMsg = "Select user to be changed";
            }
            else
            {
                string selectedUserId = dataGridView1.SelectedCells[0].Value.ToString();
                string selectedUserName = dataGridView1.SelectedCells[1].Value.ToString();
                bool selectedIsAdmin = (bool) dataGridView1.SelectedCells[2].Value;

                string text = "";
                if (selectedIsAdmin)
                {
                    text = "This action will change the role of \"" + selectedUserName + "\"\nfrom admin to regular user. Are you sure?";
                }
                else
                {
                    text = "This action will change the role of \"" + selectedUserName + "\"\nfrom regular user to admin. Are you sure?";
                }

                var mboxResponse = MessageBox.Show(this, text, "Change Role: " + selectedUserName, MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                if (mboxResponse == DialogResult.Yes)
                {
                    viewUserController.changeUserRole(selectedUserId, !selectedIsAdmin);
                    refreshForm();
                    MessageBox.Show(this, "Change Role Success", "Change User Role", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Change User Role", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }

        private void btnResetPassword_Click(object sender, EventArgs e)
        {
            string errMsg = "";

            if (dataGridView1.SelectedCells.Count == 0)
            {
                errMsg = "Select user to be reset";
            }
            else
            {
                string selectedUserId = dataGridView1.SelectedCells[0].Value.ToString();
                string selectedUserName = dataGridView1.SelectedCells[1].Value.ToString();
                bool selectedIsAdmin = (bool)dataGridView1.SelectedCells[2].Value;

                RegisterForm registerForm = new RegisterForm("Reset Password", selectedUserName);
                registerForm.ShowDialog(this);
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Reset Password", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }
    }
}
