namespace AHPApp
{
    partial class PairwiseComparisonUserControl
    {
        /// <summary> 
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary> 
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Component Designer generated code

        /// <summary> 
        /// Required method for Designer support - do not modify 
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(PairwiseComparisonUserControl));
            this.lblNumber = new System.Windows.Forms.Label();
            this.lblCriteria1 = new System.Windows.Forms.Label();
            this.lblCriteria2 = new System.Windows.Forms.Label();
            this.trackBar1 = new System.Windows.Forms.TrackBar();
            this.btnResetValue = new System.Windows.Forms.Button();
            this.lblHiddenCWId = new System.Windows.Forms.Label();
            this.toolTip1 = new System.Windows.Forms.ToolTip(this.components);
            this.lblValue = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.trackBar1)).BeginInit();
            this.SuspendLayout();
            // 
            // lblNumber
            // 
            this.lblNumber.AutoSize = true;
            this.lblNumber.Location = new System.Drawing.Point(8, 27);
            this.lblNumber.Name = "lblNumber";
            this.lblNumber.Size = new System.Drawing.Size(35, 13);
            this.lblNumber.TabIndex = 0;
            this.lblNumber.Text = "label1";
            // 
            // lblCriteria1
            // 
            this.lblCriteria1.Location = new System.Drawing.Point(49, 27);
            this.lblCriteria1.Name = "lblCriteria1";
            this.lblCriteria1.Size = new System.Drawing.Size(67, 26);
            this.lblCriteria1.TabIndex = 1;
            this.lblCriteria1.Text = "label1";
            this.lblCriteria1.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // lblCriteria2
            // 
            this.lblCriteria2.Location = new System.Drawing.Point(340, 27);
            this.lblCriteria2.Name = "lblCriteria2";
            this.lblCriteria2.Size = new System.Drawing.Size(82, 26);
            this.lblCriteria2.TabIndex = 1;
            this.lblCriteria2.Text = "label1";
            this.lblCriteria2.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // trackBar1
            // 
            this.trackBar1.BackColor = System.Drawing.SystemColors.Control;
            this.trackBar1.LargeChange = 1;
            this.trackBar1.Location = new System.Drawing.Point(122, 23);
            this.trackBar1.Maximum = 16;
            this.trackBar1.Name = "trackBar1";
            this.trackBar1.Size = new System.Drawing.Size(212, 45);
            this.trackBar1.TabIndex = 2;
            this.trackBar1.Scroll += new System.EventHandler(this.trackBar1_Scroll);
            this.trackBar1.ValueChanged += new System.EventHandler(this.trackBar1_ValueChanged);
            // 
            // btnResetValue
            // 
            this.btnResetValue.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("btnResetValue.BackgroundImage")));
            this.btnResetValue.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.btnResetValue.Location = new System.Drawing.Point(428, 22);
            this.btnResetValue.Name = "btnResetValue";
            this.btnResetValue.Size = new System.Drawing.Size(20, 23);
            this.btnResetValue.TabIndex = 3;
            this.btnResetValue.UseVisualStyleBackColor = true;
            this.btnResetValue.Click += new System.EventHandler(this.btnResetValue_Click);
            // 
            // lblHiddenCWId
            // 
            this.lblHiddenCWId.AutoSize = true;
            this.lblHiddenCWId.Location = new System.Drawing.Point(8, 40);
            this.lblHiddenCWId.Name = "lblHiddenCWId";
            this.lblHiddenCWId.Size = new System.Drawing.Size(35, 13);
            this.lblHiddenCWId.TabIndex = 4;
            this.lblHiddenCWId.Text = "label1";
            this.lblHiddenCWId.Visible = false;
            // 
            // lblValue
            // 
            this.lblValue.AutoSize = true;
            this.lblValue.BackColor = System.Drawing.Color.Transparent;
            this.lblValue.Location = new System.Drawing.Point(217, 5);
            this.lblValue.Name = "lblValue";
            this.lblValue.Size = new System.Drawing.Size(35, 13);
            this.lblValue.TabIndex = 5;
            this.lblValue.Text = "label1";
            // 
            // PairwiseComparisonUserControl
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.lblValue);
            this.Controls.Add(this.lblHiddenCWId);
            this.Controls.Add(this.btnResetValue);
            this.Controls.Add(this.trackBar1);
            this.Controls.Add(this.lblCriteria2);
            this.Controls.Add(this.lblCriteria1);
            this.Controls.Add(this.lblNumber);
            this.Name = "PairwiseComparisonUserControl";
            this.Size = new System.Drawing.Size(449, 66);
            this.Load += new System.EventHandler(this.PairwiseComparisonUserControl_Load);
            ((System.ComponentModel.ISupportInitialize)(this.trackBar1)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label lblNumber;
        private System.Windows.Forms.Label lblCriteria1;
        private System.Windows.Forms.Label lblCriteria2;
        private System.Windows.Forms.TrackBar trackBar1;
        private System.Windows.Forms.Button btnResetValue;
        private System.Windows.Forms.Label lblHiddenCWId;
        private System.Windows.Forms.ToolTip toolTip1;
        private System.Windows.Forms.Label lblValue;
    }
}
