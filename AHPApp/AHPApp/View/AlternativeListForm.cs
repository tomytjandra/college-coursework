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
    public partial class AlternativeListForm : Form
    {
        private MainForm mainForm;
        private AlternativeListController alternativeListController;
        private CriteriaController criteriaController;
        private DataView data;
        string currentTopicId;
        string currentUserName;
        bool isFormEdited;
        int selectedRowIdx;

        public AlternativeListForm()
        {
            InitializeComponent();
        }

        public string getCurrentTopicId()
        {
            return this.currentTopicId;
        }

        public string getCurrentUserName()
        {
            return this.currentUserName;
        }

        /*
        protected override bool ProcessCmdKey(ref Message msg, Keys keyData)
        {
            if (keyData == (Keys.Control | Keys.S))
            {
                saveForm();
                return true;
            }
            return base.ProcessCmdKey(ref msg, keyData);
        }
        */

        public override void Refresh()
        {
            AlternativeListForm_Load(this, new EventArgs());
            base.Refresh();
        }

        private void AlternativeListForm_Load(object sender, EventArgs e)
        {
            mainForm = (MainForm)this.MdiParent;
            alternativeListController = new AlternativeListController();
            criteriaController = new CriteriaController();
            currentTopicId = mainForm.getCurrentTopic().topicId.ToString();
            currentUserName = mainForm.getCurrentUser().userName;
            isFormEdited = false;

            refreshTable();

            if (alternativeListController.getAlternativeList(currentTopicId).Count < 1)
            {
                MessageBox.Show(this, "Please input 2-11 alternatives", "Alternative List", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        public DataGridView getDGV()
        {
            dataGridView1.DataSource = null;
            DataTable dt = new DataTable();

            int criteriaCount = 0;
            // DYNAMIC COLUMN
            dt.Columns.Add(new DataColumn("Alternative Name", typeof(string)));
            foreach (Criteria criteria in criteriaController.getCriteriaList(currentTopicId))
            {
                criteriaCount++;
                string columnName = criteria.criteriaName;
                if (criteria.criteriaUnit != "")
                {
                    columnName += " (" + criteria.criteriaUnit + ")";
                }

                if (criteria.isBoolean)
                {
                    dt.Columns.Add(new DataColumn(columnName, typeof(Boolean)));
                }
                else
                {
                    dt.Columns.Add(new DataColumn(columnName, typeof(double)));
                }
            }

            // DYNAMIC ROW
            foreach (string alternativeName in alternativeListController.getAlternativeList(currentTopicId))
            {
                DataRow row = dt.NewRow();

                row["Alternative Name"] = alternativeName;

                foreach (Criteria criteria in criteriaController.getCriteriaList(currentTopicId))
                {
                    string columnName = criteria.criteriaName;
                    if (criteria.criteriaUnit != "")
                    {
                        columnName += " (" + criteria.criteriaUnit + ")";
                    }

                    row[columnName] = alternativeListController.valueLookup(criteria.criteriaId, alternativeName);
                }
                
                dt.Rows.Add(row);
            }

            dataGridView1.DataSource = dt;
            dataGridView1.ClearSelection();
            dataGridView1.ReadOnly = true;
            return dataGridView1;
        }

        public void refreshTable()
        {
            dataGridView1.DataSource = null;
            DataTable dt = new DataTable();

            int criteriaCount = 0;
            // DYNAMIC COLUMN
            dt.Columns.Add(new DataColumn("Alternative Name", typeof(string)));
            foreach (Criteria criteria in criteriaController.getCriteriaList(currentTopicId))
            {
                criteriaCount++;
                string columnName = criteria.criteriaName;
                if (criteria.criteriaUnit != "")
                {
                    columnName += " ("+ criteria.criteriaUnit +")";
                }

                if (criteria.isBoolean)
                {
                    dt.Columns.Add(new DataColumn(columnName, typeof(Boolean)));
                }
                else
                {
                    dt.Columns.Add(new DataColumn(columnName, typeof(double)));
                }
            }
            dt.Columns.Add(new DataColumn("Created Date", typeof(string)));
            dt.Columns.Add(new DataColumn("Created By", typeof(string)));
            dt.Columns.Add(new DataColumn("Last Modified Date", typeof(string)));
            dt.Columns.Add(new DataColumn("Last Modified By", typeof(string)));

            // DYNAMIC ROW
            foreach (string alternativeName in alternativeListController.getAlternativeList(currentTopicId))
            {
                DataRow row = dt.NewRow();
                
                row["Alternative Name"] = alternativeName;

                foreach (Criteria criteria in criteriaController.getCriteriaList(currentTopicId))
                {
                    string columnName = criteria.criteriaName;
                    if (criteria.criteriaUnit != "")
                    {
                        columnName += " (" + criteria.criteriaUnit + ")";
                    }

                    row[columnName] = alternativeListController.valueLookup(criteria.criteriaId, alternativeName);
                }

                List<int> detailId = cvtAlternativeName2DetailIdList(alternativeName);

                row["Created Date"] = alternativeListController.getCreatedDetail4OneRow(detailId).ElementAt(0);
                row["Created By"] = alternativeListController.getCreatedDetail4OneRow(detailId).ElementAt(1);
                row["Last Modified Date"] = alternativeListController.getLastModifiedDetail4OneRow(detailId).ElementAt(0);
                row["Last Modified By"] = alternativeListController.getLastModifiedDetail4OneRow(detailId).ElementAt(1);

                dt.Rows.Add(row);
            }

            dataGridView1.DataSource = dt;
            dataGridView1.ClearSelection();

            dataGridView1.Columns[criteriaCount + 1].ReadOnly = true;
            dataGridView1.Columns[criteriaCount + 2].ReadOnly = true;
            dataGridView1.Columns[criteriaCount + 3].ReadOnly = true;
            dataGridView1.Columns[criteriaCount + 4].ReadOnly = true;
            dataGridView1.ReadOnly = true;
        }

        public bool isDGVContainsBlankCell()
        {
            bool isBlankCell = false;
            DataTable dt = (DataTable)dataGridView1.DataSource;

            foreach (DataRow row in dt.Rows)
            {
                foreach (DataColumn col in dt.Columns)
                {
                    if (row[col.ColumnName].ToString() == "")
                    {
                        isBlankCell = true;
                        break;
                    }
                }
            }

            return isBlankCell;
        }

        public bool isAlternativeUnique(string alternative, int rowIndex)
        {
            bool isUnique = true;

            for (int i = 0; i < dataGridView1.RowCount; i++)
            {
                if (i == rowIndex)
                {
                    continue;
                }

                if (dataGridView1[0, i].Value.ToString().ToUpper() == alternative.ToUpper())
                {
                    isUnique = false;
                    break;
                }
            }

            return isUnique;
        }

        public int cvtCriteriaName2Id(string criteriaName)
        {
            int criteriaId = 0;

            foreach (Criteria criteria in criteriaController.getCriteriaList(currentTopicId))
            {
                if (criteria.criteriaName == criteriaName)
                {
                    criteriaId = criteria.criteriaId;
                    break;
                }
            }

            return criteriaId;
        }

        public List<int> cvtAlternativeName2DetailIdList(string alternativeName)
        {
            List<int> detailIdList = new List<int>();

            foreach (DetailAlternative detailAlternative in alternativeListController.getDetailList(currentTopicId))
            {
                if (detailAlternative.alternativeName == alternativeName)
                {
                    detailIdList.Add(detailAlternative.detailId);
                }
            }

            return detailIdList;
        }

        private void btnAddRow_Click(object sender, EventArgs e)
        {
            if (dataGridView1.RowCount < 11)
            {
                //DataTable dt = (DataTable)dataGridView1.DataSource;
                //DataRow row = dt.NewRow();
                //dt.Rows.Add(row);
                //dataGridView1.DataSource = dt;
                //dataGridView1.ClearSelection();

                AddAlternativeForm addAlternativeForm = new AddAlternativeForm("Add", "", -1);
                addAlternativeForm.ShowDialog(this);

                mainForm.updateTooltipVisibility();
            }
            else
            {
                MessageBox.Show(this, "Maximum number of alternative reached", "Add New Row", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }

        private void btnEdit_Click(object sender, EventArgs e)
        {
            string errMsg = "";

            if (dataGridView1.RowCount == 0)
            {
                errMsg = "No row to be edited";
            }
            else if (dataGridView1.SelectedCells.Count == 0)
            {
                errMsg = "Select row to be edited";
            }
            else
            {
                AddAlternativeForm addAlternativeForm = new AddAlternativeForm("Edit", dataGridView1.SelectedCells[0].Value.ToString(), this.selectedRowIdx);
                addAlternativeForm.ShowDialog(this);
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Edit Alternative Row", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }

        private void btnDeleteRow_Click(object sender, EventArgs e)
        {
            string errMsg = "";

            if (dataGridView1.RowCount == 0)
            {
                errMsg = "No row to be deleted";
            }
            else if (dataGridView1.SelectedCells.Count == 0)
            {
                errMsg = "Select row to be deleted";
            }
            else
            {
                string selectedAlternativeName = dataGridView1.SelectedCells[0].Value.ToString();
                
                var mboxResponse = MessageBox.Show(this, "This action will delete the entire data \nin row \"" + selectedAlternativeName + "\". Are you sure?", "Delete Alternative: "+ selectedAlternativeName, MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                if (mboxResponse == DialogResult.Yes)
                {
                    List<int> selectedDetailId = cvtAlternativeName2DetailIdList(selectedAlternativeName);

                    foreach (int detailId in selectedDetailId)
                    {
                        alternativeListController.deleteOneDetailAlternative(detailId);
                    }

                    mainForm.updateTooltipVisibility();
                    this.Refresh();
                    mainForm.refreshAllChildrenForm();
                    MessageBox.Show(this, "Delete Success", "Delete Alternative Row", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Delete Alternative Row", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }

        // EDIT TABLE
        private string oldStringValue;
        private double oldDoubleValue;

        private void dataGridView1_DataError(object sender, DataGridViewDataErrorEventArgs e)
        {
            if (e.ColumnIndex != 0)
            {
                dataGridView1[e.ColumnIndex, e.RowIndex].Value = oldDoubleValue;
                MessageBox.Show(this, "Must be numeric (integer or decimal)", "Input Error", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }

        private void dataGridView1_CellBeginEdit(object sender, DataGridViewCellCancelEventArgs e)
        {
            if (e.ColumnIndex == 0)
            {
                oldStringValue = dataGridView1[e.ColumnIndex, e.RowIndex].Value.ToString();
            }
            else
            {
                try
                {
                    oldDoubleValue = (double)dataGridView1[e.ColumnIndex, e.RowIndex].Value;
                }
                catch
                {
                    oldDoubleValue = 0;
                }
            }
        }

        private void dataGridView1_CellValueChanged(object sender, DataGridViewCellEventArgs e)
        {
            string newValue = dataGridView1[e.ColumnIndex, e.RowIndex].Value.ToString();

            if (e.ColumnIndex == 0)
            {
                if (newValue == "")
                {
                    MessageBox.Show(this, "Alternative name must be filled", "Edit Error", MessageBoxButtons.OK, MessageBoxIcon.Hand);
                    dataGridView1[e.ColumnIndex, e.RowIndex].Value = oldStringValue;
                }
                else if (!isAlternativeUnique(newValue, e.RowIndex))
                {
                    MessageBox.Show(this, "Alternative name must be unique", "Edit Error", MessageBoxButtons.OK, MessageBoxIcon.Hand);
                    dataGridView1[e.ColumnIndex, e.RowIndex].Value = oldStringValue;
                }
                else
                {
                    isFormEdited = true;

                    foreach (int detailId in cvtAlternativeName2DetailIdList(oldStringValue))
                    {
                        alternativeListController.updateLastModified(detailId, currentUserName);
                    }
                }
            }
            else
            {
                isFormEdited = true;
            }
        }

        /*
        public bool saveForm()
        {
            string errMsg = "";
            bool returnVal = true;

            if (isDGVContainsBlankCell())
            {
                errMsg = "You haven't fill the table completely";
            }
            else if (dataGridView1.RowCount < 2)
            {
                errMsg = "Input must be between 2 and 11 rows of alternative";
            }
            else
            {
                DataTable dt = (DataTable)dataGridView1.DataSource;

                foreach (DataRow row in dt.Rows)
                {
                    string alternativeName = row["Alternative Name"].ToString();

                    foreach (DataColumn col in dt.Columns)
                    {
                        if (col.ColumnName != "Alternative Name")
                        {
                            string criteriaName = "";

                            try
                            {
                                criteriaName = col.ColumnName.Substring(0, col.ColumnName.IndexOf('(')).Trim();
                            }
                            catch
                            {
                                criteriaName = col.ColumnName;
                            }
                            
                            int criteriaId = cvtCriteriaName2Id(criteriaName);
                            double value = (double) row[col.ColumnName];

                            if (!alternativeListController.isDetailAlternativeExist(criteriaId, alternativeName))
                            {
                                alternativeListController.addOneDetailAlternative(criteriaId, alternativeName, value, currentUserName);
                            }
                            else
                            {
                                alternativeListController.editOneDetailAlternative(criteriaId, alternativeName, value);
                            }
                        }
                    }
                }

                isFormEdited = false;
                MessageBox.Show(this, "Save Success", "Save Alternative", MessageBoxButtons.OK, MessageBoxIcon.Information);
                returnVal = true;
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Save Error", MessageBoxButtons.OK, MessageBoxIcon.Hand);
                returnVal = false;
            }

            return returnVal;
        }
        

        private void btnSave_Click(object sender, EventArgs e)
        {
            saveForm();
        }
        */

        private void AlternativeListForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (isFormEdited)
            {
                var mboxResponse = MessageBox.Show(this, "Do you want to save changes?",
                "Close Alternative List", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);

                if (mboxResponse == DialogResult.Yes /*&& !saveForm()*/)
                {
                    e.Cancel = true;
                }
                else
                {
                    this.Dispose();
                }
            }
        }

        private void dataGridView1_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            this.selectedRowIdx = e.RowIndex;
        }

        private void dataGridView1_CellMouseDoubleClick(object sender, DataGridViewCellMouseEventArgs e)
        {
            try
            {
                btnEdit_Click(this, new EventArgs());
            }
            catch (Exception)
            {

            }
        }
    }
}
