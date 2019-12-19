namespace AHPApp
{
    partial class AddAlternativeUserControl
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
            this.lblCriteriaName = new System.Windows.Forms.Label();
            this.numericUpDown1 = new System.Windows.Forms.NumericUpDown();
            this.checkBox1 = new System.Windows.Forms.CheckBox();
            this.lblCriteriaUnit = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown1)).BeginInit();
            this.SuspendLayout();
            // 
            // lblCriteriaName
            // 
            this.lblCriteriaName.Location = new System.Drawing.Point(-15, 0);
            this.lblCriteriaName.Name = "lblCriteriaName";
            this.lblCriteriaName.Size = new System.Drawing.Size(131, 34);
            this.lblCriteriaName.TabIndex = 0;
            this.lblCriteriaName.Text = "label1";
            this.lblCriteriaName.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // numericUpDown1
            // 
            this.numericUpDown1.DecimalPlaces = 5;
            this.numericUpDown1.Location = new System.Drawing.Point(122, 8);
            this.numericUpDown1.Maximum = new decimal(new int[] {
            -1981284353,
            -1966660860,
            0,
            0});
            this.numericUpDown1.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            1179648});
            this.numericUpDown1.Name = "numericUpDown1";
            this.numericUpDown1.Size = new System.Drawing.Size(83, 20);
            this.numericUpDown1.TabIndex = 2;
            this.numericUpDown1.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.numericUpDown1.Value = new decimal(new int[] {
            1,
            0,
            0,
            131072});
            this.numericUpDown1.ValueChanged += new System.EventHandler(this.numericUpDown1_ValueChanged);
            this.numericUpDown1.KeyDown += new System.Windows.Forms.KeyEventHandler(this.numericUpDown1_KeyDown);
            // 
            // checkBox1
            // 
            this.checkBox1.AutoEllipsis = true;
            this.checkBox1.Location = new System.Drawing.Point(122, 11);
            this.checkBox1.Name = "checkBox1";
            this.checkBox1.Size = new System.Drawing.Size(15, 14);
            this.checkBox1.TabIndex = 3;
            this.checkBox1.UseVisualStyleBackColor = true;
            // 
            // lblCriteriaUnit
            // 
            this.lblCriteriaUnit.Location = new System.Drawing.Point(211, 0);
            this.lblCriteriaUnit.Name = "lblCriteriaUnit";
            this.lblCriteriaUnit.Size = new System.Drawing.Size(78, 34);
            this.lblCriteriaUnit.TabIndex = 0;
            this.lblCriteriaUnit.Text = "label1";
            this.lblCriteriaUnit.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.lblCriteriaUnit.Click += new System.EventHandler(this.lblCriteriaUnit_Click);
            // 
            // AddAlternativeUserControl
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.checkBox1);
            this.Controls.Add(this.numericUpDown1);
            this.Controls.Add(this.lblCriteriaUnit);
            this.Controls.Add(this.lblCriteriaName);
            this.Name = "AddAlternativeUserControl";
            this.Size = new System.Drawing.Size(266, 34);
            this.Load += new System.EventHandler(this.AddAlternativeUserControl_Load);
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown1)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Label lblCriteriaName;
        private System.Windows.Forms.NumericUpDown numericUpDown1;
        private System.Windows.Forms.CheckBox checkBox1;
        private System.Windows.Forms.Label lblCriteriaUnit;
    }
}
