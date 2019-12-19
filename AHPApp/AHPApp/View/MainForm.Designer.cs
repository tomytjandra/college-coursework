namespace AHPApp
{
    partial class MainForm
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MainForm));
            this.fileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.loadFileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.saveFileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.loginToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.registerToolStripMenuItem2 = new System.Windows.Forms.ToolStripMenuItem();
            this.viewTopicToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.backToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.criteriaListToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.criteriaWeightToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.alternativeListToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.resultToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.openAllFormToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.closeAllFormToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.helpToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.viewUserToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.userToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.changePasswordToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.logoutToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.lblUser = new System.Windows.Forms.Label();
            this.menuStrip2 = new System.Windows.Forms.MenuStrip();
            this.topicCountToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.criteriaCountToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.alternativeCountToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.menuStrip1.SuspendLayout();
            this.menuStrip2.SuspendLayout();
            this.SuspendLayout();
            // 
            // fileToolStripMenuItem
            // 
            this.fileToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.loadFileToolStripMenuItem,
            this.saveFileToolStripMenuItem});
            this.fileToolStripMenuItem.Image = ((System.Drawing.Image)(resources.GetObject("fileToolStripMenuItem.Image")));
            this.fileToolStripMenuItem.Name = "fileToolStripMenuItem";
            this.fileToolStripMenuItem.ShortcutKeyDisplayString = "";
            this.fileToolStripMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.F)));
            this.fileToolStripMenuItem.Size = new System.Drawing.Size(131, 20);
            this.fileToolStripMenuItem.Text = "&File";
            // 
            // loadFileToolStripMenuItem
            // 
            this.loadFileToolStripMenuItem.Image = ((System.Drawing.Image)(resources.GetObject("loadFileToolStripMenuItem.Image")));
            this.loadFileToolStripMenuItem.Name = "loadFileToolStripMenuItem";
            this.loadFileToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.loadFileToolStripMenuItem.Text = "Load File";
            this.loadFileToolStripMenuItem.Click += new System.EventHandler(this.loadFileToolStripMenuItem_Click);
            // 
            // saveFileToolStripMenuItem
            // 
            this.saveFileToolStripMenuItem.Image = ((System.Drawing.Image)(resources.GetObject("saveFileToolStripMenuItem.Image")));
            this.saveFileToolStripMenuItem.Name = "saveFileToolStripMenuItem";
            this.saveFileToolStripMenuItem.Size = new System.Drawing.Size(121, 22);
            this.saveFileToolStripMenuItem.Text = "Save File";
            this.saveFileToolStripMenuItem.Click += new System.EventHandler(this.saveFileToolStripMenuItem_Click);
            // 
            // loginToolStripMenuItem1
            // 
            this.loginToolStripMenuItem1.Image = ((System.Drawing.Image)(resources.GetObject("loginToolStripMenuItem1.Image")));
            this.loginToolStripMenuItem1.Name = "loginToolStripMenuItem1";
            this.loginToolStripMenuItem1.Size = new System.Drawing.Size(65, 20);
            this.loginToolStripMenuItem1.Text = "Login";
            this.loginToolStripMenuItem1.Click += new System.EventHandler(this.loginToolStripMenuItem1_Click);
            // 
            // registerToolStripMenuItem2
            // 
            this.registerToolStripMenuItem2.Image = ((System.Drawing.Image)(resources.GetObject("registerToolStripMenuItem2.Image")));
            this.registerToolStripMenuItem2.Name = "registerToolStripMenuItem2";
            this.registerToolStripMenuItem2.Size = new System.Drawing.Size(77, 20);
            this.registerToolStripMenuItem2.Text = "Register";
            this.registerToolStripMenuItem2.Click += new System.EventHandler(this.registerToolStripMenuItem2_Click);
            // 
            // viewTopicToolStripMenuItem
            // 
            this.viewTopicToolStripMenuItem.Image = ((System.Drawing.Image)(resources.GetObject("viewTopicToolStripMenuItem.Image")));
            this.viewTopicToolStripMenuItem.Name = "viewTopicToolStripMenuItem";
            this.viewTopicToolStripMenuItem.Size = new System.Drawing.Size(131, 20);
            this.viewTopicToolStripMenuItem.Text = "&View Topic";
            this.viewTopicToolStripMenuItem.Click += new System.EventHandler(this.topicToolStripMenuItem_Click);
            // 
            // backToolStripMenuItem
            // 
            this.backToolStripMenuItem.Image = ((System.Drawing.Image)(resources.GetObject("backToolStripMenuItem.Image")));
            this.backToolStripMenuItem.Name = "backToolStripMenuItem";
            this.backToolStripMenuItem.Size = new System.Drawing.Size(131, 20);
            this.backToolStripMenuItem.Text = "&Back to Main Menu";
            this.backToolStripMenuItem.Click += new System.EventHandler(this.backToolStripMenuItem_Click);
            // 
            // criteriaListToolStripMenuItem1
            // 
            this.criteriaListToolStripMenuItem1.Name = "criteriaListToolStripMenuItem1";
            this.criteriaListToolStripMenuItem1.Size = new System.Drawing.Size(131, 19);
            this.criteriaListToolStripMenuItem1.Text = "&Criteria List";
            this.criteriaListToolStripMenuItem1.Click += new System.EventHandler(this.criteriaListToolStripMenuItem1_Click);
            // 
            // criteriaWeightToolStripMenuItem1
            // 
            this.criteriaWeightToolStripMenuItem1.Name = "criteriaWeightToolStripMenuItem1";
            this.criteriaWeightToolStripMenuItem1.Size = new System.Drawing.Size(131, 19);
            this.criteriaWeightToolStripMenuItem1.Text = "Criteria &Weight";
            this.criteriaWeightToolStripMenuItem1.Click += new System.EventHandler(this.criteriaWeightToolStripMenuItem_Click);
            // 
            // alternativeListToolStripMenuItem1
            // 
            this.alternativeListToolStripMenuItem1.Name = "alternativeListToolStripMenuItem1";
            this.alternativeListToolStripMenuItem1.Size = new System.Drawing.Size(131, 19);
            this.alternativeListToolStripMenuItem1.Text = "&Alternative List";
            this.alternativeListToolStripMenuItem1.Click += new System.EventHandler(this.alternativeListToolStripMenuItem1_Click);
            // 
            // resultToolStripMenuItem1
            // 
            this.resultToolStripMenuItem1.Name = "resultToolStripMenuItem1";
            this.resultToolStripMenuItem1.Size = new System.Drawing.Size(131, 19);
            this.resultToolStripMenuItem1.Text = "Result";
            this.resultToolStripMenuItem1.Click += new System.EventHandler(this.resultToolStripMenuItem1_Click);
            // 
            // openAllFormToolStripMenuItem1
            // 
            this.openAllFormToolStripMenuItem1.Image = ((System.Drawing.Image)(resources.GetObject("openAllFormToolStripMenuItem1.Image")));
            this.openAllFormToolStripMenuItem1.Name = "openAllFormToolStripMenuItem1";
            this.openAllFormToolStripMenuItem1.Size = new System.Drawing.Size(131, 20);
            this.openAllFormToolStripMenuItem1.Text = "&Open All Form";
            this.openAllFormToolStripMenuItem1.Click += new System.EventHandler(this.openAllFormToolStripMenuItem_Click);
            // 
            // closeAllFormToolStripMenuItem1
            // 
            this.closeAllFormToolStripMenuItem1.Image = ((System.Drawing.Image)(resources.GetObject("closeAllFormToolStripMenuItem1.Image")));
            this.closeAllFormToolStripMenuItem1.Name = "closeAllFormToolStripMenuItem1";
            this.closeAllFormToolStripMenuItem1.Size = new System.Drawing.Size(131, 20);
            this.closeAllFormToolStripMenuItem1.Text = "Close All Form";
            this.closeAllFormToolStripMenuItem1.Click += new System.EventHandler(this.closeAllFormToolStripMenuItem1_Click);
            // 
            // helpToolStripMenuItem
            // 
            this.helpToolStripMenuItem.Alignment = System.Windows.Forms.ToolStripItemAlignment.Right;
            this.helpToolStripMenuItem.Image = ((System.Drawing.Image)(resources.GetObject("helpToolStripMenuItem.Image")));
            this.helpToolStripMenuItem.Name = "helpToolStripMenuItem";
            this.helpToolStripMenuItem.Size = new System.Drawing.Size(131, 20);
            this.helpToolStripMenuItem.Text = "&Progress";
            this.helpToolStripMenuItem.Click += new System.EventHandler(this.helpToolStripMenuItem_Click);
            // 
            // menuStrip1
            // 
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.fileToolStripMenuItem,
            this.loginToolStripMenuItem1,
            this.registerToolStripMenuItem2,
            this.viewUserToolStripMenuItem1,
            this.viewTopicToolStripMenuItem,
            this.backToolStripMenuItem,
            this.criteriaListToolStripMenuItem1,
            this.criteriaWeightToolStripMenuItem1,
            this.alternativeListToolStripMenuItem1,
            this.resultToolStripMenuItem1,
            this.openAllFormToolStripMenuItem1,
            this.closeAllFormToolStripMenuItem1,
            this.helpToolStripMenuItem,
            this.userToolStripMenuItem1});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(800, 24);
            this.menuStrip1.TabIndex = 1;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // viewUserToolStripMenuItem1
            // 
            this.viewUserToolStripMenuItem1.Image = ((System.Drawing.Image)(resources.GetObject("viewUserToolStripMenuItem1.Image")));
            this.viewUserToolStripMenuItem1.Name = "viewUserToolStripMenuItem1";
            this.viewUserToolStripMenuItem1.Size = new System.Drawing.Size(86, 20);
            this.viewUserToolStripMenuItem1.Text = "View &User";
            this.viewUserToolStripMenuItem1.Click += new System.EventHandler(this.viewUserToolStripMenuItem1_Click);
            // 
            // userToolStripMenuItem1
            // 
            this.userToolStripMenuItem1.Alignment = System.Windows.Forms.ToolStripItemAlignment.Right;
            this.userToolStripMenuItem1.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.changePasswordToolStripMenuItem,
            this.logoutToolStripMenuItem});
            this.userToolStripMenuItem1.Image = ((System.Drawing.Image)(resources.GetObject("userToolStripMenuItem1.Image")));
            this.userToolStripMenuItem1.Name = "userToolStripMenuItem1";
            this.userToolStripMenuItem1.Size = new System.Drawing.Size(131, 20);
            this.userToolStripMenuItem1.Text = "Hi, ";
            // 
            // changePasswordToolStripMenuItem
            // 
            this.changePasswordToolStripMenuItem.Image = ((System.Drawing.Image)(resources.GetObject("changePasswordToolStripMenuItem.Image")));
            this.changePasswordToolStripMenuItem.Name = "changePasswordToolStripMenuItem";
            this.changePasswordToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.changePasswordToolStripMenuItem.Text = "Change Password";
            this.changePasswordToolStripMenuItem.Click += new System.EventHandler(this.changePasswordToolStripMenuItem_Click);
            // 
            // logoutToolStripMenuItem
            // 
            this.logoutToolStripMenuItem.Image = ((System.Drawing.Image)(resources.GetObject("logoutToolStripMenuItem.Image")));
            this.logoutToolStripMenuItem.Name = "logoutToolStripMenuItem";
            this.logoutToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.logoutToolStripMenuItem.Text = "Logout";
            this.logoutToolStripMenuItem.Click += new System.EventHandler(this.logoutToolStripMenuItem_Click);
            // 
            // lblUser
            // 
            this.lblUser.AutoSize = true;
            this.lblUser.BackColor = System.Drawing.Color.WhiteSmoke;
            this.lblUser.Cursor = System.Windows.Forms.Cursors.Arrow;
            this.lblUser.Font = new System.Drawing.Font("Segoe UI", 20.25F, ((System.Drawing.FontStyle)((System.Drawing.FontStyle.Bold | System.Drawing.FontStyle.Italic))), System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblUser.ForeColor = System.Drawing.Color.Black;
            this.lblUser.Location = new System.Drawing.Point(12, 42);
            this.lblUser.Name = "lblUser";
            this.lblUser.Size = new System.Drawing.Size(61, 37);
            this.lblUser.TabIndex = 3;
            this.lblUser.Text = "Hi, ";
            this.lblUser.Visible = false;
            // 
            // menuStrip2
            // 
            this.menuStrip2.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.menuStrip2.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.topicCountToolStripMenuItem,
            this.criteriaCountToolStripMenuItem,
            this.alternativeCountToolStripMenuItem});
            this.menuStrip2.Location = new System.Drawing.Point(0, 426);
            this.menuStrip2.Name = "menuStrip2";
            this.menuStrip2.Size = new System.Drawing.Size(800, 24);
            this.menuStrip2.TabIndex = 5;
            this.menuStrip2.Text = "menuStrip2";
            // 
            // topicCountToolStripMenuItem
            // 
            this.topicCountToolStripMenuItem.Name = "topicCountToolStripMenuItem";
            this.topicCountToolStripMenuItem.Size = new System.Drawing.Size(64, 20);
            this.topicCountToolStripMenuItem.Text = "Topic(s):";
            // 
            // criteriaCountToolStripMenuItem
            // 
            this.criteriaCountToolStripMenuItem.Name = "criteriaCountToolStripMenuItem";
            this.criteriaCountToolStripMenuItem.Size = new System.Drawing.Size(76, 20);
            this.criteriaCountToolStripMenuItem.Text = "Criteria(s): ";
            // 
            // alternativeCountToolStripMenuItem
            // 
            this.alternativeCountToolStripMenuItem.Name = "alternativeCountToolStripMenuItem";
            this.alternativeCountToolStripMenuItem.Size = new System.Drawing.Size(92, 20);
            this.alternativeCountToolStripMenuItem.Text = "Alternative(s):";
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.Black;
            this.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("$this.BackgroundImage")));
            this.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.menuStrip1);
            this.Controls.Add(this.menuStrip2);
            this.Controls.Add(this.lblUser);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.IsMdiContainer = true;
            this.MainMenuStrip = this.menuStrip1;
            this.Name = "MainForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Analytic Hierarchy Process";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.MainMenu_FormClosing);
            this.Load += new System.EventHandler(this.MainForm_Load);
            this.SizeChanged += new System.EventHandler(this.MainMenu_SizeChanged);
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.menuStrip2.ResumeLayout(false);
            this.menuStrip2.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ToolStripMenuItem fileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem loadFileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem saveFileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem loginToolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem registerToolStripMenuItem2;
        private System.Windows.Forms.ToolStripMenuItem viewTopicToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem backToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem criteriaListToolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem criteriaWeightToolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem alternativeListToolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem resultToolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem openAllFormToolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem closeAllFormToolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem helpToolStripMenuItem;
        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.Label lblUser;
        private System.Windows.Forms.ToolStripMenuItem userToolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem changePasswordToolStripMenuItem;
        private System.Windows.Forms.MenuStrip menuStrip2;
        private System.Windows.Forms.ToolStripMenuItem criteriaCountToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem alternativeCountToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem topicCountToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem logoutToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem viewUserToolStripMenuItem1;
    }
}

