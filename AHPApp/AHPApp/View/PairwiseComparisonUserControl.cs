using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace AHPApp
{
    public partial class PairwiseComparisonUserControl : UserControl
    {
        List<double> convertWeightValue = new List<double> { 9, 8, 7, 6, 5, 4, 3, 2, 1, 1 / 2.0, 1 / 3.0, 1 / 4.0, 1 / 5.0, 1 / 6.0, 1 / 7.0, 1 / 8.0, 1 / 9.0 };
        List<string> convertWeight4Tooltip = new List<string> { "9", "8", "7", "6", "5", "4", "3", "2", "1", "1/2", "1/3", "1/4", "1/5", "1/6", "1/7", "1/8", "1/9" };
        int criteriaWeightId, criteria1Id, criteria2Id;
        CriteriaRankingForm cwForm;

        public PairwiseComparisonUserControl(int countUC, int criteriaWeightId, int criteria1Id, int criteria2Id, string criteria1Name, string criteria2Name, double importanceLevel)
        {
            InitializeComponent();
            resetTrackbar2DefaultValue();
            

            this.criteriaWeightId = criteriaWeightId;
            this.criteria1Id = criteria1Id;
            this.criteria2Id = criteria2Id;
            lblNumber.Text = countUC.ToString() + ".";
            lblCriteria1.Text = criteria1Name.Replace(' ', '\n');
            lblCriteria2.Text = criteria2Name.Replace(' ', '\n');
            trackBar1.Value = convertImportanceLevel2TrackbarValue(importanceLevel);

        }

        private void btnResetValue_Click(object sender, EventArgs e)
        {
            resetTrackbar2DefaultValue();
            cwForm = (CriteriaRankingForm)this.FindForm();
            cwForm.triggerUpdateLabelConsistencyInfo();
        }

        public int convertImportanceLevel2TrackbarValue(double importanceLevel)
        {
            int idxFound = -1;
            for (int i = 0; i < convertWeightValue.Count; i++)
            {
                if (Math.Round(convertWeightValue.ElementAt(i), 2) == Math.Round(importanceLevel, 2))
                {
                    idxFound = i;
                    break;
                }
            }
            return idxFound;
        }

        public void resetTrackbar2DefaultValue()
        {
            trackBar1.Value = (int)Math.Ceiling((trackBar1.Minimum + trackBar1.Maximum) / 2.0);
        }

        public double getImportanceLevel()
        {
            return convertWeightValue.ElementAt(trackBar1.Value);
        }

        public string getImportanceLevelTooltip()
        {
            return convertWeight4Tooltip.ElementAt(trackBar1.Value);
        }

        public int getCriteriaWeightId()
        {
            return this.criteriaWeightId;
        }

        private void trackBar1_Scroll(object sender, EventArgs e)
        {
            lblValue.Text = getImportanceLevelTooltip() + " x";
            cwForm = (CriteriaRankingForm)this.FindForm();
            cwForm.triggerUpdateLabelConsistencyInfo();
        }

        private void trackBar1_ValueChanged(object sender, EventArgs e)
        {
            lblValue.Text = getImportanceLevelTooltip() + " x";
        }

        private void PairwiseComparisonUserControl_Load(object sender, EventArgs e)
        {

        }

        public int getCriteria1Id()
        {
            return this.criteria1Id;
        }

        public int getCriteria2Id()
        {
            return this.criteria2Id;
        }
        
    }
}
