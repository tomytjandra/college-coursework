namespace AHPApp
{
    partial class ResultUserControl
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
            this.lblValue = new System.Windows.Forms.Label();
            this.lblAlternative = new System.Windows.Forms.Label();
            this.lblNumber = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // lblValue
            // 
            this.lblValue.BackColor = System.Drawing.Color.Transparent;
            this.lblValue.Location = new System.Drawing.Point(41, 14);
            this.lblValue.Name = "lblValue";
            this.lblValue.Size = new System.Drawing.Size(80, 23);
            this.lblValue.TabIndex = 0;
            this.lblValue.Text = "label1";
            this.lblValue.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.lblValue.Click += new System.EventHandler(this.lblValue_Click);
            // 
            // lblAlternative
            // 
            this.lblAlternative.BackColor = System.Drawing.Color.Transparent;
            this.lblAlternative.Location = new System.Drawing.Point(41, -2);
            this.lblAlternative.Name = "lblAlternative";
            this.lblAlternative.Size = new System.Drawing.Size(121, 23);
            this.lblAlternative.TabIndex = 0;
            this.lblAlternative.Text = "label1";
            this.lblAlternative.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // lblNumber
            // 
            this.lblNumber.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblNumber.ImageAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.lblNumber.Location = new System.Drawing.Point(-13, 8);
            this.lblNumber.Name = "lblNumber";
            this.lblNumber.Size = new System.Drawing.Size(48, 23);
            this.lblNumber.TabIndex = 0;
            this.lblNumber.Text = "label1";
            this.lblNumber.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // ResultUserControl
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.lblNumber);
            this.Controls.Add(this.lblAlternative);
            this.Controls.Add(this.lblValue);
            this.Name = "ResultUserControl";
            this.Size = new System.Drawing.Size(186, 39);
            this.Load += new System.EventHandler(this.ResultUserControl_Load);
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Label lblValue;
        private System.Windows.Forms.Label lblAlternative;
        private System.Windows.Forms.Label lblNumber;
    }
}
