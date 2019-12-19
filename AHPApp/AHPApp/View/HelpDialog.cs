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
    public partial class HelpDialog : Form
    {
        private MainForm mainForm;
        private MainController mainController;
        private AlternativeListController alternativeListController;
        private List<string> status = new List<string> { "not done", "done" };

        public HelpDialog()
        {
            InitializeComponent();
        }

        public override void Refresh()
        {
            HelpDialog_Load(this, new EventArgs());
            base.Refresh();
        }

        private void HelpDialog_Load(object sender, EventArgs e)
        {
            mainForm = (MainForm)this.MdiParent;
            mainController = new MainController();
            alternativeListController = new AlternativeListController();
            Topic currentTopic = mainForm.getCurrentTopic();
            string currentTopicId = "";

            if (currentTopic != null)
            {
                cbStep1.Checked = true;
                lblStep1.Text = status.ElementAt(1);

                currentTopicId = currentTopic.topicId.ToString();
                int countCriteria = mainController.countCriteria(currentTopicId);
                
                if (countCriteria >= 3 && countCriteria <= 11)
                {
                    cbStep2.Checked = true;
                    lblStep2.Text = status.ElementAt(1);
                }
                else
                {
                    cbStep2.Checked = false;
                    cbStep3.Checked = true;
                    
                    lblStep2.Text = status.ElementAt(0);
                    lblStep3.Text = status.ElementAt(0);
                }
                
                if (!mainController.isAllCriteriaWeightDefault(currentTopicId))
                {
                    cbStep3.Checked = true;
                    lblStep3.Text = status.ElementAt(1);
                }
                else
                {
                    cbStep3.Checked = false;
                    lblStep3.Text = status.ElementAt(0);
                }

                if (alternativeListController.getAlternativeList(currentTopicId).Count >= 2)
                {
                    cbStep4.Checked = true;
                    cbStep5.Checked = true;

                    lblStep4.Text = status.ElementAt(1);
                    lblStep5.Text = status.ElementAt(1);
                }
                else
                {
                    cbStep4.Checked = false;
                    cbStep5.Checked = false;

                    lblStep4.Text = status.ElementAt(0);
                    lblStep5.Text = status.ElementAt(0);
                }
            }
            else
            {
                cbStep1.Checked = false;
                cbStep2.Checked = false;
                cbStep3.Checked = false;
                cbStep4.Checked = false;
                cbStep5.Checked = false;

                lblStep1.Text = status.ElementAt(0);
                lblStep2.Text = status.ElementAt(0);
                lblStep3.Text = status.ElementAt(0);
                lblStep4.Text = status.ElementAt(0);
                lblStep5.Text = status.ElementAt(0);
            }
        }

        private void btnOk_Click(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}
