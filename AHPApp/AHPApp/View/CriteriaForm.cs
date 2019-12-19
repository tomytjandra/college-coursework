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
    public partial class CriteriaForm : Form
    {
        private MainForm mainForm;
        private CriteriaController criteriaController;
        private AlternativeListController alternativeListController;
        private DataView data;
        string currentTopicId;
        string currentUserName;

        private bool isIsBooleanChanged;

        public CriteriaForm()
        {
            InitializeComponent();
        }

        private void CriteriaForm_Load(object sender, EventArgs e)
        {
            mainForm = (MainForm)this.MdiParent;
            criteriaController = new CriteriaController();
            alternativeListController = new AlternativeListController();
            currentTopicId = mainForm.getCurrentTopic().topicId.ToString();
            currentUserName = mainForm.getCurrentUser().userName;
            isIsBooleanChanged = false;

            refreshForm();

            if (dataGridView1.RowCount < 3)
            {
                MessageBox.Show(this, "Please input 3-6 criterias", "Criteria List", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private void refreshForm()
        {
            data = criteriaController.getCriteriaData(currentTopicId);
            dataGridView1.DataSource = data;
            dataGridView1.ClearSelection();
            dataGridView1.Columns[0].Visible = false;
            dataGridView1.Columns[1].Visible = false;

            criteriaController.autoInsertCriteriaWeight(currentTopicId);

            txtCriteriaName.Text = "";
            txtCriteriaUnit.Text = "";
            cbIsFewerBetter.Checked = false;
            cbIsBoolean.Checked = false;

            mainForm.refreshAllChildrenForm();
            mainForm.updateTooltipVisibility();

            if (dataGridView1.RowCount < 3)
            {
                mainForm.closeAllChildrenFormExcept(typeof(CriteriaForm), typeof(HelpDialog));
            }
        }

        // BUTTON EVENT
        private void btnAdd_Click(object sender, EventArgs e)
        {
            string criteriaName = txtCriteriaName.Text;
            string criteriaUnit = txtCriteriaUnit.Text;
            bool isFewerBetter = cbIsFewerBetter.Checked;
            bool isBoolean = cbIsBoolean.Checked;
            string errMsg = "";
            int countCriteria = criteriaController.getCriteriaList(currentTopicId).Count;
            
            if (countCriteria >= 6)
            {
                errMsg = "Maximum number of criteria reached";
            }
            else if (criteriaName == "")
            {
                errMsg = "Criteria Name must be filled";
            }
            else if (criteriaName.Length < 3 || criteriaName.Length > 30)
            {
                errMsg = "Criteria Name length must be between 3 and 30";
            }
            else if (!criteriaController.isCriteriaUnique(currentTopicId, criteriaName))
            {
                errMsg = "Criteria Name must be unique";
            }
            else
            {
                int criteriaId = criteriaController.addCriteria(currentTopicId, criteriaName, criteriaUnit, isFewerBetter, isBoolean, currentUserName);

                foreach (string alternativeName in alternativeListController.getAlternativeList(currentTopicId))
                {
                    alternativeListController.addOneDetailAlternative(criteriaId, alternativeName, 0, currentUserName);
                }

                refreshForm();

                string msg = "Add Success";

                if (countCriteria == 2)
                {
                    msg += ". Now you can determine\nCriteria Weight and add Alternative List.";
                }

                MessageBox.Show(this, msg, "Add Criteria", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Add Criteria", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }

        private void btnEdit_Click(object sender, EventArgs e)
        {
            string criteriaName = txtCriteriaName.Text;
            string criteriaUnit = txtCriteriaUnit.Text;
            bool isFewerBetter = cbIsFewerBetter.Checked;
            bool isBoolean = cbIsBoolean.Checked;
            string errMsg = "";

            if (dataGridView1.SelectedCells.Count == 0)
            {
                errMsg = "Select criteria to be edited";
            }
            else if (criteriaName == "")
            {
                errMsg = "Criteria Name must be filled";
            }
            else if (criteriaName.Length < 3 || criteriaName.Length > 30)
            {
                errMsg = "Criteria Name length must be between 3 and 30";
            }
            else
            {
                string selectedCriteriaName = dataGridView1.SelectedCells[2].Value.ToString();
                string selectedCriteriaUnit = dataGridView1.SelectedCells[3].Value.ToString();
                string selectedIsFewerBetter = dataGridView1.SelectedCells[4].Value.ToString();
                string selectedIsBoolean = dataGridView1.SelectedCells[5].Value.ToString();

                if (criteriaName == selectedCriteriaName && criteriaUnit == selectedCriteriaUnit && isFewerBetter.ToString() == selectedIsFewerBetter && isBoolean.ToString() == selectedIsBoolean)
                {
                    errMsg = "Nothing is edited";
                }
                else if (!criteriaController.isCriteriaUnique(currentTopicId, criteriaName) && criteriaName != selectedCriteriaName)
                {
                    errMsg = "Criteria Name must be unique";
                }
                else
                {
                    string selectedCriteriaId = dataGridView1.SelectedCells[0].Value.ToString();

                    criteriaController.editCriteria(selectedCriteriaId, criteriaName, criteriaUnit, isFewerBetter, isBoolean, currentUserName);

                    if (isIsBooleanChanged)
                    {
                        if (isBoolean)
                        {
                            alternativeListController.fromNotBoolean2Boolean(selectedCriteriaId);
                        }
                        else
                        {
                            alternativeListController.fromBoolean2NotBoolean(selectedCriteriaId);
                        }
                    }

                    refreshForm();
                    MessageBox.Show(this, "Edit Success", "Edit Criteria", MessageBoxButtons.OK, MessageBoxIcon.Information);

                    isIsBooleanChanged = false;
                }
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Edit Criteria", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }

        private void btnDelete_Click(object sender, EventArgs e)
        {
            string errMsg = "";

            if (dataGridView1.SelectedCells.Count == 0)
            {
                errMsg = "Select criteria to be deleted";
            }
            else
            {
                string selectedCriteriaId = dataGridView1.SelectedCells[0].Value.ToString();
                string selectedCriteriaName = dataGridView1.SelectedCells[2].Value.ToString();
                //DeleteConfirmation deleteConfirmation = new DeleteConfirmation("Criteria", selectedCriteriaName);
                //var response = deleteConfirmation.ShowDialog();

                //if (response == DialogResult.OK)
                //{
                //    criteriaController.deleteCriteria(selectedCriteriaId);
                //    refreshForm();

                //    MessageBox.Show(this, "Delete Success", "Delete Criteria", MessageBoxButtons.OK, MessageBoxIcon.Information);
                //}

                var mboxResponse = MessageBox.Show(this, "This action will delete the entire existing data \nin criteria \"" + selectedCriteriaName + "\". Are you sure?", "Delete Criteria: " + selectedCriteriaName, MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                if (mboxResponse == DialogResult.Yes)
                {
                    criteriaController.deleteCriteria(selectedCriteriaId);
                    alternativeListController.deleteAllDetailAlternativePerCriteria(selectedCriteriaId);

                    refreshForm();

                    MessageBox.Show(this, "Delete Success", "Delete Criteria", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Delete Criteria", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }

        // DATAGRID EVENT
        private void dataGridView1_DataBindingComplete(object sender, DataGridViewBindingCompleteEventArgs e)
        {
            dataGridView1.ClearSelection();
        }

        private void dataGridView1_CellMouseClick(object sender, DataGridViewCellMouseEventArgs e)
        {
            try
            {
                txtCriteriaName.Text = dataGridView1.SelectedCells[2].Value.ToString();
                txtCriteriaUnit.Text = dataGridView1.SelectedCells[3].Value.ToString();
                string isFewerBetter = dataGridView1.SelectedCells[4].Value.ToString();
                string isBoolean = dataGridView1.SelectedCells[5].Value.ToString();

                if (isFewerBetter == "False")
                {
                    cbIsFewerBetter.Checked = false;
                }
                else
                {
                    cbIsFewerBetter.Checked = true;
                }

                if (isBoolean == "False")
                {
                    cbIsBoolean.Checked = false;
                }
                else
                {
                    cbIsBoolean.Checked = true;
                }
            }
            catch (Exception)
            {
                dataGridView1.ClearSelection();
            }
        }

        private void dataGridView1_CellMouseLeave(object sender, DataGridViewCellEventArgs e)
        {
            try
            {
                txtCriteriaName.Text = dataGridView1.SelectedCells[2].Value.ToString();
                txtCriteriaUnit.Text = dataGridView1.SelectedCells[3].Value.ToString();
                string isFewerBetter = dataGridView1.SelectedCells[4].Value.ToString();
                string isBoolean = dataGridView1.SelectedCells[5].Value.ToString();

                if (isFewerBetter == "False")
                {
                    cbIsFewerBetter.Checked = false;
                }
                else
                {
                    cbIsFewerBetter.Checked = true;
                }

                if (isBoolean == "False")
                {
                    cbIsBoolean.Checked = false;
                }
                else
                {
                    cbIsBoolean.Checked = true;
                }
            }
            catch (Exception)
            {
                dataGridView1.ClearSelection();
            }
        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }

        private void dataGridView1_ColumnHeaderMouseClick(object sender, DataGridViewCellMouseEventArgs e)
        {
            dataGridView1.ClearSelection();

            txtCriteriaName.Text = "";
            txtCriteriaUnit.Text = "";
            cbIsFewerBetter.Checked = false;
            cbIsBoolean.Checked = false;
        }
        
        private void label4_MouseHover(object sender, EventArgs e)
        {
            toolTip1.Show("Tick the box if the fewer value is inputted to this criteria, the better it will be.\nEg. Price, the cheaper the better.", this.label4, 30000);
        }

        private void label5_MouseHover(object sender, EventArgs e)
        {
            toolTip2.Show("Tick the box if the value of criteria is either Yes or No (boolean)", this.label5, 30000);
        }

        private void cbIsBoolean_CheckedChanged(object sender, EventArgs e)
        {
            isIsBooleanChanged = true;
        }
    }
}
