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
    public partial class CriteriaRankingForm : Form
    {
        private MainForm mainForm;
        private CriteriaWeightController criteriaWeightController;
        private CriteriaController criteriaController;
        string currentTopicId;
        
        public CriteriaRankingForm()
        {
            InitializeComponent();
        }

        protected override bool ProcessCmdKey(ref Message msg, Keys keyData)
        {
            if (keyData == (Keys.Control | Keys.S))
            {
                saveWeight();
                return true;
            }
            return base.ProcessCmdKey(ref msg, keyData);
        }

        public bool isWeightChanged()
        {
            List<double> savedWeightList = criteriaWeightController.getImportanceLevelList(currentTopicId);
            List<double> currentWeightList = new List<double>();

            foreach (PairwiseComparisonUserControl pairwiseComparisonUserControl in flowLayoutPanel1.Controls)
            {
                double importanceLevel = pairwiseComparisonUserControl.getImportanceLevel();
                currentWeightList.Add(importanceLevel);
            }

            // Compare two list
            bool isChanged = false;

            for (int i = 0; i < savedWeightList.Count; i++)
            {
                if (Math.Round(savedWeightList.ElementAt(i), 2) != Math.Round(currentWeightList.ElementAt(i), 2))
                {
                    isChanged = true;
                    break;
                }
            }

            return isChanged;
        }

        public override void Refresh()
        {
            CriteriaRankingForm_Load(this, new EventArgs());
            base.Refresh();
        }

        private void CriteriaRankingForm_Load(object sender, EventArgs e)
        {
            mainForm = (MainForm)this.MdiParent;
            criteriaWeightController = new CriteriaWeightController();
            try
            {
                currentTopicId = mainForm.getCurrentTopic().topicId.ToString();
            }
            catch
            {
                this.Close();
            }
            

            criteriaController = new CriteriaController();
            criteriaController.autoInsertCriteriaWeight(currentTopicId);

            loadDynamicUI();

            triggerUpdateLabelConsistencyInfo();
        }

        public void loadDynamicUI()
        {
            flowLayoutPanel1.Controls.Clear();

            List<CriteriaWeight> criteriaWeightList = criteriaWeightController.getCriteriaWeightListName(currentTopicId);

            for (int i = 0; i < criteriaWeightList.Count; i++)
            {
                int countUC = flowLayoutPanel1.Controls.Count + 1;
                int criteriaWeightId = criteriaWeightList.ElementAt(i).criteriaWeightId;
                int criteria1Id = criteriaWeightList.ElementAt(i).criteria1Id;
                int criteria2Id = criteriaWeightList.ElementAt(i).criteria2Id;
                string criteria1Name = criteriaWeightList.ElementAt(i).criteria1Name;
                string criteria2Name = criteriaWeightList.ElementAt(i).criteria2Name;
                double importanceLevel = criteriaWeightList.ElementAt(i).importanceLevel;

                PairwiseComparisonUserControl pairwiseComparisonUserControl = new PairwiseComparisonUserControl(countUC, criteriaWeightId, criteria1Id, criteria2Id, criteria1Name, criteria2Name, importanceLevel);
                pairwiseComparisonUserControl.Parent = flowLayoutPanel1;
                flowLayoutPanel1.Controls.Add(pairwiseComparisonUserControl);
            }
        }

        private void btnResetValueDefault_Click(object sender, EventArgs e)
        {
            foreach (PairwiseComparisonUserControl pairwiseComparisonUserControl in flowLayoutPanel1.Controls)
            {
                pairwiseComparisonUserControl.resetTrackbar2DefaultValue();
            }
            triggerUpdateLabelConsistencyInfo();
        }

        public double[][] cloneMatrix(double[][] originalMatrix, int sizeMatrix)
        {
            double[][] result = new double[sizeMatrix][];

            for (int i = 0; i < sizeMatrix; i++)
            {
                result[i] = new double[sizeMatrix];
                for (int j = 0; j < sizeMatrix; j++)
                {
                    result[i][j] = originalMatrix[i][j];
                }
            }

            return result;
        }

        public bool isInputConsistent()
        {
            // 1. Pairwise Comparison Matrix

            // 1.1. Get list of criteria Id for mapping
            List<int> criteriaIdList = new List<int>();

            foreach (Criteria criteria in criteriaController.getCriteriaList(currentTopicId))
            {
                criteriaIdList.Add(criteria.criteriaId);
            }

            int countCriteria = criteriaIdList.Count;

            // 1.2. Mapping criteriaId to index
            Dictionary<int, int> criteriaId2Idx = new Dictionary<int, int>();
            for (int i = 0; i < countCriteria; i++)
            {
                criteriaId2Idx.Add(criteriaIdList.ElementAt(i), i);
            }
        
            // 1.3. Create list of data for each pcuc            
            // [[criteria1id, criteria2id, importancelvl], [criteria1id, criteria2id, importancelvl], ...]
            List<List<double>> pcucData = new List<List<double>>();
            foreach (PairwiseComparisonUserControl pairwiseComparisonUserControl in flowLayoutPanel1.Controls)
            {
                int criteria1Id = pairwiseComparisonUserControl.getCriteria1Id();
                int criteria2Id = pairwiseComparisonUserControl.getCriteria2Id();
                double importanceLevel = pairwiseComparisonUserControl.getImportanceLevel();

                int criteria1Idx, criteria2Idx;
                criteriaId2Idx.TryGetValue(criteria1Id, out criteria1Idx);
                criteriaId2Idx.TryGetValue(criteria2Id, out criteria2Idx);
                pcucData.Add(new List<double>() { criteria1Idx, criteria2Idx, importanceLevel });
            }

            // 1.4. Prepare blank matrix with value 1 in main diagonal
            double[][] pcMatrix = new double[countCriteria][];
            for (int i = 0; i < countCriteria; i++)
            {
                pcMatrix[i] = new double[countCriteria];
                for (int j = 0; j < countCriteria; j++)
                {
                    if (i == j)
                    {
                        pcMatrix[i][j] = 1;
                    }
                }
            }

            // 1.5. Fill other value in matrix
            foreach (var pcuc in pcucData)
            {
                int criteria1Idx = Convert.ToInt32(pcuc.ElementAt(0));
                int criteria2Idx = Convert.ToInt32(pcuc.ElementAt(1));
                double importanceLevel = pcuc.ElementAt(2);

                pcMatrix[criteria1Idx][criteria2Idx] = importanceLevel;
                pcMatrix[criteria2Idx][criteria1Idx] = 1 / importanceLevel;
            }

            // 2. Normalize Matrix
            double[][] normalizedPcMatrix = cloneMatrix(pcMatrix, countCriteria);

            // 2.1. Sum by Column
            double[] colSum = new double[countCriteria];
            for (int i = 0; i < countCriteria; i++)
            {
                double tempSum = 0;
                for (int j = 0; j < countCriteria; j++)
                {
                    tempSum += pcMatrix[j][i];
                }
                colSum[i] = tempSum;
            }
            
            // 2.2. Divide each cell by sum of the column
            for (int i = 0; i < countCriteria; i++)
            {
                for (int j = 0; j < countCriteria; j++)
                {
                    normalizedPcMatrix[i][j] = normalizedPcMatrix[i][j] / colSum[j];
                }
            }

            // 3. Calculate Priority Vector
            double[] priorityVec = new double[countCriteria];
            for (int i = 0; i < countCriteria; i++)
            {
                double tempSum = 0;
                for (int j = 0; j < countCriteria; j++)
                {
                    tempSum += normalizedPcMatrix[i][j];
                }
                priorityVec[i] = tempSum / countCriteria;
            }

            // 4. Consistency Vector = (Matrix * Priority Vector) / Priority Vector[i]
            double[] consistencyVec = new double[countCriteria];
            for (int i = 0; i < countCriteria; i++)
            {
                consistencyVec[i] = 0;
                for (int j = 0; j < countCriteria; j++)
                {
                    consistencyVec[i] += pcMatrix[i][j] * priorityVec[j];
                }
                consistencyVec[i] = consistencyVec[i] / priorityVec[i];
            }

            // 5. Compute Consistence Idx
            double lambdaMax = 0;
            for (int i = 0; i < countCriteria; i++)
            {
                lambdaMax += consistencyVec[i];
            }
            lambdaMax /= countCriteria;
            double consistenceIdx = (lambdaMax - countCriteria) / (countCriteria - 1);

            // 6. Compute Consistency Ratio
            double[] randomIdx = new double[] { 0, 0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.51 };
            double consistencyRatio = consistenceIdx / randomIdx[countCriteria];

            return consistencyRatio < 0.2;
        }

        public void triggerUpdateLabelConsistencyInfo()
        {
            if (isInputConsistent())
            {
                lblConsistencyInfo.Text = "Your input is consistent";
                lblConsistencyInfo.ForeColor = Color.DarkGreen;
                btnSave.Enabled = true;
            }
            else
            {
                lblConsistencyInfo.Text = "Your input is inconsistent";
                lblConsistencyInfo.ForeColor = Color.Red;
                btnSave.Enabled = false;
            }
        }

        public bool saveWeight()
        {
            if (isInputConsistent())
            {
                foreach (PairwiseComparisonUserControl pairwiseComparisonUserControl in flowLayoutPanel1.Controls)
                {
                    int criteriaWeightId = pairwiseComparisonUserControl.getCriteriaWeightId();
                    int criteria1Id = pairwiseComparisonUserControl.getCriteria1Id();
                    int criteria2Id = pairwiseComparisonUserControl.getCriteria2Id();
                    double importanceLevel = pairwiseComparisonUserControl.getImportanceLevel();

                    criteriaWeightController.editOneCriteriaWeight(criteriaWeightId, importanceLevel);
                }

                MessageBox.Show(this, "Save Success", "Save Criteria Ranking", MessageBoxButtons.OK, MessageBoxIcon.Information);
                return true;
            }
            else
            {
                loadDynamicUI();
                triggerUpdateLabelConsistencyInfo();
                MessageBox.Show(this, "Your input is inconsistent.\nInput will be reset to last saved state.", "Save Criteria Ranking", MessageBoxButtons.OK, MessageBoxIcon.Hand);
                return false;
            }
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            saveWeight();
            mainForm.refreshAllChildrenForm();
        }

        private void btnResetValueDB_Click(object sender, EventArgs e)
        {
            loadDynamicUI();
            triggerUpdateLabelConsistencyInfo();
        }

        private void CriteriaRankingForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (isWeightChanged())
            {
                var mboxResponse = MessageBox.Show(this, "Do you want to save changes?",
                "Close Criteria Ranking", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);

                if (mboxResponse == DialogResult.Yes && !saveWeight())
                {
                    e.Cancel = true;
                }
                else
                {
                    this.Dispose();
                }
            }
        }

        private void btnResetValueDB_MouseHover(object sender, EventArgs e)
        {
            toolTip1.SetToolTip(btnResetValueDB, "Reset all value based on last saved data");
        }

        private void btnResetValueDefault_MouseHover(object sender, EventArgs e)
        {
            toolTip2.SetToolTip(btnResetValueDefault, "Reset all trackbar to center (1 x)");
        }

        private void btnSave_MouseHover(object sender, EventArgs e)
        {
            toolTip3.SetToolTip(btnSave, "Save current weight");
        }

        private void lblConsistencyInfo_Click(object sender, EventArgs e)
        {

        }
    }
}