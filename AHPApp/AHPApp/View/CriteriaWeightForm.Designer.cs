namespace AHPApp
{
    partial class CriteriaRankingForm
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

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(CriteriaRankingForm));
            this.flowLayoutPanel1 = new System.Windows.Forms.FlowLayoutPanel();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.btnResetValueDefault = new System.Windows.Forms.Button();
            this.btnSave = new System.Windows.Forms.Button();
            this.btnResetValueDB = new System.Windows.Forms.Button();
            this.toolTip1 = new System.Windows.Forms.ToolTip(this.components);
            this.toolTip2 = new System.Windows.Forms.ToolTip(this.components);
            this.toolTip3 = new System.Windows.Forms.ToolTip(this.components);
            this.lblConsistencyInfo = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // flowLayoutPanel1
            // 
            this.flowLayoutPanel1.AutoScroll = true;
            this.flowLayoutPanel1.FlowDirection = System.Windows.Forms.FlowDirection.TopDown;
            this.flowLayoutPanel1.Location = new System.Drawing.Point(12, 24);
            this.flowLayoutPanel1.Name = "flowLayoutPanel1";
            this.flowLayoutPanel1.Size = new System.Drawing.Size(476, 198);
            this.flowLayoutPanel1.TabIndex = 3;
            this.flowLayoutPanel1.WrapContents = false;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(70, 8);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(75, 13);
            this.label1.TabIndex = 1;
            this.label1.Text = "First Criteria";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.Location = new System.Drawing.Point(223, 8);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(47, 13);
            this.label2.TabIndex = 1;
            this.label2.Text = "Weight";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.Location = new System.Drawing.Point(352, 8);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(94, 13);
            this.label3.TabIndex = 1;
            this.label3.Text = "Second Criteria";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label4.Location = new System.Drawing.Point(17, 8);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(23, 13);
            this.label4.TabIndex = 1;
            this.label4.Text = "No";
            // 
            // btnResetValueDefault
            // 
            this.btnResetValueDefault.Location = new System.Drawing.Point(198, 251);
            this.btnResetValueDefault.Name = "btnResetValueDefault";
            this.btnResetValueDefault.Size = new System.Drawing.Size(102, 23);
            this.btnResetValueDefault.TabIndex = 1;
            this.btnResetValueDefault.Text = "&Default Value";
            this.btnResetValueDefault.UseVisualStyleBackColor = true;
            this.btnResetValueDefault.Click += new System.EventHandler(this.btnResetValueDefault_Click);
            this.btnResetValueDefault.MouseHover += new System.EventHandler(this.btnResetValueDefault_MouseHover);
            // 
            // btnSave
            // 
            this.btnSave.Location = new System.Drawing.Point(344, 251);
            this.btnSave.Name = "btnSave";
            this.btnSave.Size = new System.Drawing.Size(102, 23);
            this.btnSave.TabIndex = 2;
            this.btnSave.Text = "&Save";
            this.btnSave.UseVisualStyleBackColor = true;
            this.btnSave.Click += new System.EventHandler(this.btnSave_Click);
            this.btnSave.MouseHover += new System.EventHandler(this.btnSave_MouseHover);
            // 
            // btnResetValueDB
            // 
            this.btnResetValueDB.Location = new System.Drawing.Point(53, 251);
            this.btnResetValueDB.Name = "btnResetValueDB";
            this.btnResetValueDB.Size = new System.Drawing.Size(102, 23);
            this.btnResetValueDB.TabIndex = 0;
            this.btnResetValueDB.Text = "&Back";
            this.btnResetValueDB.UseVisualStyleBackColor = true;
            this.btnResetValueDB.Click += new System.EventHandler(this.btnResetValueDB_Click);
            this.btnResetValueDB.MouseHover += new System.EventHandler(this.btnResetValueDB_MouseHover);
            // 
            // lblConsistencyInfo
            // 
            this.lblConsistencyInfo.Font = new System.Drawing.Font("Segoe UI", 11.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblConsistencyInfo.Location = new System.Drawing.Point(12, 225);
            this.lblConsistencyInfo.Name = "lblConsistencyInfo";
            this.lblConsistencyInfo.Size = new System.Drawing.Size(476, 23);
            this.lblConsistencyInfo.TabIndex = 4;
            this.lblConsistencyInfo.Text = "label5";
            this.lblConsistencyInfo.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            this.lblConsistencyInfo.Click += new System.EventHandler(this.lblConsistencyInfo_Click);
            // 
            // CriteriaRankingForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(500, 286);
            this.Controls.Add(this.lblConsistencyInfo);
            this.Controls.Add(this.btnSave);
            this.Controls.Add(this.btnResetValueDB);
            this.Controls.Add(this.btnResetValueDefault);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.flowLayoutPanel1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "CriteriaRankingForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Criteria Weight";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.CriteriaRankingForm_FormClosing);
            this.Load += new System.EventHandler(this.CriteriaRankingForm_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.FlowLayoutPanel flowLayoutPanel1;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Button btnResetValueDefault;
        private System.Windows.Forms.Button btnSave;
        private System.Windows.Forms.Button btnResetValueDB;
        private System.Windows.Forms.ToolTip toolTip1;
        private System.Windows.Forms.ToolTip toolTip2;
        private System.Windows.Forms.ToolTip toolTip3;
        private System.Windows.Forms.Label lblConsistencyInfo;
    }
}