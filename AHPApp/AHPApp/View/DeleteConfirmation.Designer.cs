namespace AHPApp
{
    partial class DeleteConfirmation
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(DeleteConfirmation));
            this.pbIcon = new System.Windows.Forms.PictureBox();
            this.lblWarning = new System.Windows.Forms.Label();
            this.lblCaptcha = new System.Windows.Forms.Label();
            this.btnConfirmDelete = new System.Windows.Forms.Button();
            this.txtCaptcha = new System.Windows.Forms.TextBox();
            this.btnResetCaptcha = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.pbIcon)).BeginInit();
            this.SuspendLayout();
            // 
            // pbIcon
            // 
            this.pbIcon.Location = new System.Drawing.Point(104, 12);
            this.pbIcon.Name = "pbIcon";
            this.pbIcon.Size = new System.Drawing.Size(56, 50);
            this.pbIcon.TabIndex = 0;
            this.pbIcon.TabStop = false;
            // 
            // lblWarning
            // 
            this.lblWarning.AutoSize = true;
            this.lblWarning.Location = new System.Drawing.Point(8, 74);
            this.lblWarning.Name = "lblWarning";
            this.lblWarning.Size = new System.Drawing.Size(35, 13);
            this.lblWarning.TabIndex = 1;
            this.lblWarning.Text = "label1";
            // 
            // lblCaptcha
            // 
            this.lblCaptcha.AutoSize = true;
            this.lblCaptcha.Font = new System.Drawing.Font("Segoe Print", 12F, ((System.Drawing.FontStyle)((System.Drawing.FontStyle.Bold | System.Drawing.FontStyle.Italic))), System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblCaptcha.Location = new System.Drawing.Point(53, 115);
            this.lblCaptcha.Name = "lblCaptcha";
            this.lblCaptcha.Size = new System.Drawing.Size(60, 28);
            this.lblCaptcha.TabIndex = 2;
            this.lblCaptcha.Text = "label1";
            // 
            // btnConfirmDelete
            // 
            this.btnConfirmDelete.Location = new System.Drawing.Point(85, 181);
            this.btnConfirmDelete.Name = "btnConfirmDelete";
            this.btnConfirmDelete.Size = new System.Drawing.Size(75, 23);
            this.btnConfirmDelete.TabIndex = 1;
            this.btnConfirmDelete.Text = "&Delete";
            this.btnConfirmDelete.UseVisualStyleBackColor = true;
            this.btnConfirmDelete.Click += new System.EventHandler(this.btnConfirmDelete_Click);
            // 
            // txtCaptcha
            // 
            this.txtCaptcha.Location = new System.Drawing.Point(58, 151);
            this.txtCaptcha.Name = "txtCaptcha";
            this.txtCaptcha.Size = new System.Drawing.Size(129, 20);
            this.txtCaptcha.TabIndex = 0;
            this.txtCaptcha.MouseEnter += new System.EventHandler(this.txtCaptcha_MouseEnter);
            // 
            // btnResetCaptcha
            // 
            this.btnResetCaptcha.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("btnResetCaptcha.BackgroundImage")));
            this.btnResetCaptcha.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Zoom;
            this.btnResetCaptcha.Location = new System.Drawing.Point(162, 118);
            this.btnResetCaptcha.Name = "btnResetCaptcha";
            this.btnResetCaptcha.Size = new System.Drawing.Size(25, 25);
            this.btnResetCaptcha.TabIndex = 2;
            this.btnResetCaptcha.UseVisualStyleBackColor = true;
            this.btnResetCaptcha.Click += new System.EventHandler(this.btnResetCaptcha_Click);
            // 
            // DeleteConfirmation
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(255, 212);
            this.Controls.Add(this.btnResetCaptcha);
            this.Controls.Add(this.txtCaptcha);
            this.Controls.Add(this.btnConfirmDelete);
            this.Controls.Add(this.lblCaptcha);
            this.Controls.Add(this.lblWarning);
            this.Controls.Add(this.pbIcon);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "DeleteConfirmation";
            this.ShowIcon = false;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "Delete";
            ((System.ComponentModel.ISupportInitialize)(this.pbIcon)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.PictureBox pbIcon;
        private System.Windows.Forms.Label lblWarning;
        private System.Windows.Forms.Label lblCaptcha;
        private System.Windows.Forms.Button btnConfirmDelete;
        private System.Windows.Forms.TextBox txtCaptcha;
        private System.Windows.Forms.Button btnResetCaptcha;
    }
}