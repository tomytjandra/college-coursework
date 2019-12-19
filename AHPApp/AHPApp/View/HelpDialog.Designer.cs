namespace AHPApp
{
    partial class HelpDialog
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(HelpDialog));
            this.lblHelp = new System.Windows.Forms.Label();
            this.btnOk = new System.Windows.Forms.Button();
            this.cbStep1 = new System.Windows.Forms.CheckBox();
            this.cbStep2 = new System.Windows.Forms.CheckBox();
            this.cbStep3 = new System.Windows.Forms.CheckBox();
            this.cbStep4 = new System.Windows.Forms.CheckBox();
            this.cbStep5 = new System.Windows.Forms.CheckBox();
            this.lblStep1 = new System.Windows.Forms.Label();
            this.lblStep2 = new System.Windows.Forms.Label();
            this.lblStep3 = new System.Windows.Forms.Label();
            this.lblStep4 = new System.Windows.Forms.Label();
            this.lblStep5 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // lblHelp
            // 
            this.lblHelp.AutoSize = true;
            this.lblHelp.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblHelp.Location = new System.Drawing.Point(13, 13);
            this.lblHelp.Name = "lblHelp";
            this.lblHelp.Size = new System.Drawing.Size(243, 120);
            this.lblHelp.TabIndex = 0;
            this.lblHelp.Text = "Step:\r\n1. Select Topic\r\n2. Input Criteria (min. 3)\r\n3. Determine Criteria Weight\r" +
    "\n4. Input Alternative Detail (min. 2)\r\n5. See the Result\r\n";
            // 
            // btnOk
            // 
            this.btnOk.Location = new System.Drawing.Point(134, 160);
            this.btnOk.Name = "btnOk";
            this.btnOk.Size = new System.Drawing.Size(75, 23);
            this.btnOk.TabIndex = 1;
            this.btnOk.Text = "&Ok";
            this.btnOk.UseVisualStyleBackColor = true;
            this.btnOk.Click += new System.EventHandler(this.btnOk_Click);
            // 
            // cbStep1
            // 
            this.cbStep1.AutoSize = true;
            this.cbStep1.Enabled = false;
            this.cbStep1.Location = new System.Drawing.Point(261, 38);
            this.cbStep1.Name = "cbStep1";
            this.cbStep1.Size = new System.Drawing.Size(15, 14);
            this.cbStep1.TabIndex = 2;
            this.cbStep1.UseVisualStyleBackColor = true;
            // 
            // cbStep2
            // 
            this.cbStep2.AutoSize = true;
            this.cbStep2.Enabled = false;
            this.cbStep2.Location = new System.Drawing.Point(261, 58);
            this.cbStep2.Name = "cbStep2";
            this.cbStep2.Size = new System.Drawing.Size(15, 14);
            this.cbStep2.TabIndex = 2;
            this.cbStep2.UseVisualStyleBackColor = true;
            // 
            // cbStep3
            // 
            this.cbStep3.AutoSize = true;
            this.cbStep3.Enabled = false;
            this.cbStep3.Location = new System.Drawing.Point(261, 78);
            this.cbStep3.Name = "cbStep3";
            this.cbStep3.Size = new System.Drawing.Size(15, 14);
            this.cbStep3.TabIndex = 2;
            this.cbStep3.UseVisualStyleBackColor = true;
            // 
            // cbStep4
            // 
            this.cbStep4.AutoSize = true;
            this.cbStep4.Enabled = false;
            this.cbStep4.Location = new System.Drawing.Point(261, 98);
            this.cbStep4.Name = "cbStep4";
            this.cbStep4.Size = new System.Drawing.Size(15, 14);
            this.cbStep4.TabIndex = 2;
            this.cbStep4.UseVisualStyleBackColor = true;
            // 
            // cbStep5
            // 
            this.cbStep5.AutoSize = true;
            this.cbStep5.Enabled = false;
            this.cbStep5.Location = new System.Drawing.Point(261, 118);
            this.cbStep5.Name = "cbStep5";
            this.cbStep5.Size = new System.Drawing.Size(15, 14);
            this.cbStep5.TabIndex = 2;
            this.cbStep5.UseVisualStyleBackColor = true;
            // 
            // lblStep1
            // 
            this.lblStep1.AutoSize = true;
            this.lblStep1.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblStep1.Location = new System.Drawing.Point(258, 36);
            this.lblStep1.Name = "lblStep1";
            this.lblStep1.Size = new System.Drawing.Size(68, 16);
            this.lblStep1.TabIndex = 3;
            this.lblStep1.Text = "not done";
            this.lblStep1.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // lblStep2
            // 
            this.lblStep2.AutoSize = true;
            this.lblStep2.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblStep2.Location = new System.Drawing.Point(258, 56);
            this.lblStep2.Name = "lblStep2";
            this.lblStep2.Size = new System.Drawing.Size(68, 16);
            this.lblStep2.TabIndex = 3;
            this.lblStep2.Text = "not done";
            this.lblStep2.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // lblStep3
            // 
            this.lblStep3.AutoSize = true;
            this.lblStep3.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblStep3.Location = new System.Drawing.Point(258, 75);
            this.lblStep3.Name = "lblStep3";
            this.lblStep3.Size = new System.Drawing.Size(68, 16);
            this.lblStep3.TabIndex = 3;
            this.lblStep3.Text = "not done";
            this.lblStep3.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // lblStep4
            // 
            this.lblStep4.AutoSize = true;
            this.lblStep4.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblStep4.Location = new System.Drawing.Point(258, 95);
            this.lblStep4.Name = "lblStep4";
            this.lblStep4.Size = new System.Drawing.Size(68, 16);
            this.lblStep4.TabIndex = 3;
            this.lblStep4.Text = "not done";
            this.lblStep4.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // lblStep5
            // 
            this.lblStep5.AutoSize = true;
            this.lblStep5.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblStep5.Location = new System.Drawing.Point(258, 115);
            this.lblStep5.Name = "lblStep5";
            this.lblStep5.Size = new System.Drawing.Size(68, 16);
            this.lblStep5.TabIndex = 3;
            this.lblStep5.Text = "not done";
            this.lblStep5.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // HelpDialog
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.Control;
            this.ClientSize = new System.Drawing.Size(336, 195);
            this.Controls.Add(this.lblStep5);
            this.Controls.Add(this.lblStep4);
            this.Controls.Add(this.lblStep3);
            this.Controls.Add(this.lblStep2);
            this.Controls.Add(this.lblStep1);
            this.Controls.Add(this.cbStep5);
            this.Controls.Add(this.cbStep4);
            this.Controls.Add(this.cbStep3);
            this.Controls.Add(this.cbStep2);
            this.Controls.Add(this.cbStep1);
            this.Controls.Add(this.btnOk);
            this.Controls.Add(this.lblHelp);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "HelpDialog";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Progress";
            this.Load += new System.EventHandler(this.HelpDialog_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label lblHelp;
        private System.Windows.Forms.Button btnOk;
        private System.Windows.Forms.CheckBox cbStep1;
        private System.Windows.Forms.CheckBox cbStep2;
        private System.Windows.Forms.CheckBox cbStep3;
        private System.Windows.Forms.CheckBox cbStep4;
        private System.Windows.Forms.CheckBox cbStep5;
        private System.Windows.Forms.Label lblStep1;
        private System.Windows.Forms.Label lblStep2;
        private System.Windows.Forms.Label lblStep3;
        private System.Windows.Forms.Label lblStep4;
        private System.Windows.Forms.Label lblStep5;
    }
}