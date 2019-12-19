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
    public partial class TopicForm : Form
    {
        private MainForm mainForm;
        private TopicController topicController;
        private AlternativeListController alternativeListController;
        private DataView data;
        private User currentUser;

        public TopicForm()
        {
            InitializeComponent();
        }

        private void TopicForm_Load(object sender, EventArgs e)
        {
            mainForm = (MainForm)this.MdiParent;
            topicController = new TopicController();
            alternativeListController = new AlternativeListController();
            currentUser = mainForm.getCurrentUser();
            refreshForm();
        }

        private void refreshForm()
        {
            if (currentUser.isAdmin == true)
            {
                data = topicController.getTopicData("");
            }
            else
            {
                data = topicController.getTopicData(currentUser.userName);
            }
            
            dataGridView1.DataSource = data;
            dataGridView1.ClearSelection();
            dataGridView1.Columns[0].Visible = false;

            if (currentUser.isAdmin == true)
            {
                dataGridView1.Columns[3].Visible = true;
            }
            else
            {
                dataGridView1.Columns[3].Visible = false;
            }

            txtTopic.Text = "";
        }

        // BUTTON EVENT
        private void btnAdd_Click(object sender, EventArgs e)
        {
            string topic = txtTopic.Text;
            string errMsg = "";

            if (topic == "")
            {
                errMsg = "Must be filled";
            }
            else if (topic.Length < 3 || topic.Length > 30)
            {
                errMsg = "Length must be between 3 and 30";
            }
            else if (!topicController.isTopicUnique(topic))
            {
                errMsg = "Must be unique";
            }
            else
            {
                topicController.addTopic(topic, currentUser.userName);
                refreshForm();
                mainForm.updateTooltipVisibility();
                MessageBox.Show(this, "Add Success", "Add Topic", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Add Topic", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }

        private void btnEdit_Click(object sender, EventArgs e)
        {
            string topic = txtTopic.Text;
            string errMsg = "";

            if (dataGridView1.SelectedCells.Count == 0)
            {
                errMsg = "Select topic to be edited";
            }
            else if (topic == "")
            {
                errMsg = "Must be filled";
            }
            else if (topic.Length < 3 || topic.Length > 30)
            {
                errMsg = "Length must be between 3 and 30";
            }
            else if (!topicController.isTopicUnique(topic))
            {
                errMsg = "Must be unique";
            }
            else {
                string selectedTopicId = dataGridView1.SelectedCells[0].Value.ToString();

                topicController.editTopic(selectedTopicId, topic, currentUser.userName);

                refreshForm();
                MessageBox.Show(this, "Edit Success", "Edit Topic", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Edit Topic", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }

        private void btnDelete_Click(object sender, EventArgs e)
        {
            string errMsg = "";

            if (dataGridView1.SelectedCells.Count == 0)
            {
                errMsg = "Select topic to be deleted";
            }
            else
            {
                string selectedTopicId = dataGridView1.SelectedCells[0].Value.ToString();
                string selectedTopicName = dataGridView1.SelectedCells[1].Value.ToString();

                //DeleteConfirmation deleteConfirmation = new DeleteConfirmation("Topic", selectedTopicName);
                //var response = deleteConfirmation.ShowDialog();

                //if (response == DialogResult.OK)
                //{
                //    topicController.deleteTopic(selectedTopicId);
                //    refreshForm();

                //    MessageBox.Show(this, "Delete Success", "Delete Topic", MessageBoxButtons.OK, MessageBoxIcon.Information);
                //}

                var mboxResponse = MessageBox.Show(this, "This action will delete the entire existing data \nin topic \""+ selectedTopicName +"\". Are you sure?", "Delete Topic: " + selectedTopicName, MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                if (mboxResponse == DialogResult.Yes)
                {
                    topicController.deleteTopic(selectedTopicId);
                    refreshForm();
                    mainForm.updateTooltipVisibility();
                    MessageBox.Show(this, "Delete Success", "Delete Topic", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Delete Topic", MessageBoxButtons.OK, MessageBoxIcon.Hand);
            }
        }

        private void btnAccess_Click(object sender, EventArgs e)
        {
            string errMsg = "";

            if (dataGridView1.SelectedCells.Count == 0)
            {
                errMsg = "Select topic to be accessed";
            }
            else
            {
                int selectedTopicId = Convert.ToInt32(dataGridView1.SelectedCells[0].Value.ToString());
                string selectedTopicName = dataGridView1.SelectedCells[1].Value.ToString();
                Topic selectedTopic = new Topic(selectedTopicId, selectedTopicName);
                mainForm.setCurrentTopic(selectedTopic);

                MessageBox.Show(this, "Access to " + selectedTopicName, "Access Topic", MessageBoxButtons.OK, MessageBoxIcon.Information);
                mainForm.Text = "Analytic Hierarchy Process: " + selectedTopicName;
                mainForm.refreshAllChildrenForm();
                this.Close();

                int countAlternative = alternativeListController.getAlternativeList(selectedTopicId.ToString()).Count;
                if (countAlternative >= 2)
                {
                    mainForm.openResultForm();
                }
            }

            if (errMsg != "")
            {
                MessageBox.Show(this, errMsg, "Access Topic", MessageBoxButtons.OK, MessageBoxIcon.Hand);
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
                txtTopic.Text = dataGridView1.SelectedCells[1].Value.ToString();
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
                txtTopic.Text = dataGridView1.SelectedCells[1].Value.ToString();
            }
            catch (Exception)
            {
                dataGridView1.ClearSelection();
            }
        }

        private void dataGridView1_ColumnHeaderMouseClick(object sender, DataGridViewCellMouseEventArgs e)
        {
            dataGridView1.ClearSelection();
            txtTopic.Text = "";
        }

        private void dataGridView1_CellMouseDoubleClick(object sender, DataGridViewCellMouseEventArgs e)
        {
            try
            {
                int selectedTopicId = Convert.ToInt32(dataGridView1.SelectedCells[0].Value.ToString());
                string selectedTopicName = dataGridView1.SelectedCells[1].Value.ToString();
                Topic selectedTopic = new Topic(selectedTopicId, selectedTopicName);
                mainForm.setCurrentTopic(selectedTopic);

                MessageBox.Show(this, "Access to " + selectedTopicName, "Access Topic", MessageBoxButtons.OK, MessageBoxIcon.Information);
                mainForm.Text = "Analytic Hierarchy Process: " + selectedTopicName;
                mainForm.refreshAllChildrenForm();
                this.Close();

                int countAlternative = alternativeListController.getAlternativeList(selectedTopicId.ToString()).Count;
                if (countAlternative >= 2)
                {
                    mainForm.openResultForm();
                }
            } catch (Exception)
            {

            }
        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }
    }
}