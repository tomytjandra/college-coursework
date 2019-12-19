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
    public partial class AddAlternativeForm : Form
    {
        private MainForm mainForm;
        private AlternativeListForm alternativeListForm;
        private CriteriaController criteriaController;
        private AlternativeListController alternativeListController;
        private string currentTopicId;
        private string currentUserName;

        public string action;
        private string selectedAlternativeName;
        private int selectedRowIdx;

        public AddAlternativeForm(string action, string selectedAlternativeName, int selectedRowIdx)
        {
            InitializeComponent();
            this.action = action;
            this.selectedAlternativeName = selectedAlternativeName;
            this.selectedRowIdx = selectedRowIdx;
        }

        public override void Refresh()
        {
            AddAlternativeForm_Load(this, new EventArgs());
            base.Refresh();
        }

        private void AddAlternativeForm_Load(object sender, EventArgs e)
        {
            foreach (var form in this.Owner.MdiChildren)
            {
                if (form.GetType() == typeof(AlternativeListForm))
                {
                    alternativeListForm = (AlternativeListForm)form;
                }
            }

            mainForm = (MainForm)this.Owner;
            criteriaController = new CriteriaController();
            alternativeListController = new AlternativeListController();
            currentTopicId = alternativeListForm.getCurrentTopicId();
            currentUserName = alternativeListForm.getCurrentUserName();
            
            if (action == "Edit")
            {
                this.Text = "Edit Alternative: " + selectedAlternativeName;
                txtAlternativeName.Text = selectedAlternativeName;
                btnAdd.Visible = false;
                btnEdit.Visible = true;
            }
            else if (action == "Add")
            {
                this.Text = "Add Alternative";
                txtAlternativeName.Text = "";
                btnAdd.Visible = true;
                btnEdit.Visible = false;
            }

            flowLayoutPanel1.Controls.Clear();
            foreach (Criteria criteria in criteriaController.getCriteriaList(currentTopicId))
            {
                int criteriaId = criteria.criteriaId;
                string criteriaName = criteria.criteriaName;
                string criteriaUnit = criteria.criteriaUnit;
                bool isBoolean = criteria.isBoolean;
                double value = 0;

                if (action == "Edit")
                {
                    value = alternativeListController.valueLookup(criteriaId, selectedAlternativeName);
                }

                AddAlternativeUserControl addAlternativeUserControl = new AddAlternativeUserControl(criteriaId, criteriaName, criteriaUnit, isBoolean, value);
                addAlternativeUserControl.Parent = flowLayoutPanel1;
                flowLayoutPanel1.Controls.Add(addAlternativeUserControl);
            }
        }

        public void resetForm()
        {
            this.Refresh();
            txtAlternativeName.Text = "";
            foreach (AddAlternativeUserControl addAlternativeUserControl in flowLayoutPanel1.Controls)
            {
                addAlternativeUserControl.setValue2Default();
            }
        }

        private void btnAdd_Click(object sender, EventArgs e)
        {
            string errMsg = "";
            string inputtedAlternativeName = txtAlternativeName.Text;

            if (inputtedAlternativeName == "")
            {
                errMsg = "Alternative Name must be filled";
            }
            else if (alternativeListController.countCertainAlternativeName(currentTopicId, inputtedAlternativeName) > 0)
            {
                errMsg = "Alternative Name must be unique";
            }
            else
            {
                foreach (AddAlternativeUserControl addAlternativeUserControl in flowLayoutPanel1.Controls)
                {
                    int criteriaId = addAlternativeUserControl.getCriteria().criteriaId;
                    double value = addAlternativeUserControl.getValue();

                    alternativeListController.addOneDetailAlternative(criteriaId, inputtedAlternativeName, value, currentUserName);
                }

                resetForm();
                alternativeListForm.Refresh();
                mainForm.refreshAllChildrenForm();

                int countAlternative = alternativeListController.getAlternativeList(currentTopicId).Count;
                string msg = "Add Success";

                if (countAlternative == 2)
                {
                    msg += ". Now you can see the final result.";
                }

                mainForm.updateTooltipVisibility();
                MessageBox.Show(this, msg, "Add Alternative", MessageBoxButtons.OK, MessageBoxIcon.Information);

                if (countAlternative == 11)
                {
                    MessageBox.Show(this, "Maximum number of alternative reached", "Add New Row", MessageBoxButtons.OK, MessageBoxIcon.Hand);
                    this.Close();
                }
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Add Alternative", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }

        private void btnEdit_Click(object sender, EventArgs e)
        {
            string errMsg = "";
            string inputtedAlternativeName = txtAlternativeName.Text;
            
            if (inputtedAlternativeName == "")
            {
                errMsg = "Alternative Name must be filled";
            }
            else if (!alternativeListForm.isAlternativeUnique(inputtedAlternativeName, selectedRowIdx))
            {
                errMsg = "Alternative Name must be unique";
            }
            else
            {
                foreach (AddAlternativeUserControl addAlternativeUserControl in flowLayoutPanel1.Controls)
                {
                    int criteriaId = addAlternativeUserControl.getCriteria().criteriaId;
                    double value = addAlternativeUserControl.getValue();

                    alternativeListController.editOneDetailAlternative(criteriaId, selectedAlternativeName, inputtedAlternativeName, value, currentUserName);
                }

                this.Close();
                alternativeListForm.Refresh();
                mainForm.refreshAllChildrenForm();
                MessageBox.Show(this, "Edit Success", "Edit Alternative", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Edit Alternative", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }

        public void txtAlternativeName_KeyDown(object sender, KeyEventArgs e)
        {
            if (action == "Add" && e.KeyCode == Keys.Enter)
            {
                btnAdd_Click(this, new EventArgs());
            }
            else if (action == "Edit" && e.KeyCode == Keys.Enter)
            {
                btnEdit_Click(this, new EventArgs());
            }
        }
    }
}
