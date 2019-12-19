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
    public partial class MainForm : Form
    {
        private MainController mainController;
        private TopicController topicController;
        private AlternativeListController alternativeListController;
        private Topic currentTopic = null;
        private User currentUser = null;

        public MainForm()
        {
            InitializeComponent();
            mainController = new MainController();
            topicController = new TopicController();
            alternativeListController = new AlternativeListController();

            // Auto Login
            // currentUser = new User("admin", true);
            // currentTopic = new Topic(1, "Test Comparison");

            this.WindowState = FormWindowState.Maximized;

            //topicToolStripMenuItem.Visible = false;
            updateTooltipVisibility();

            // Prevent window flickering
            //this.SetStyle(
            //    ControlStyles.AllPaintingInWmPaint |
            //    ControlStyles.DoubleBuffer,
            //    true);
        }

        public AlternativeListForm getAlternativeListForm()
        {
            AlternativeListForm alternativeListForm = alternativeListToolStripMenuItem_Click(this, new EventArgs());
            return alternativeListForm;
        }

        public void refreshAllChildrenForm()
        {
            foreach (var form in this.MdiChildren)
            {
                form.Refresh();
            }
        }

        public void closeAllChildrenFormExcept(Type FormType1, Type FormType2)
        {
            foreach (var form in this.MdiChildren)
            {
                if (form.GetType() != FormType1 && form.GetType() != FormType2)
                {
                    form.Close();
                }
            }
        }
        
        public void updateTooltipVisibility()
        {
            // FIRST PAGE, BEFORE LOGIN
            fileToolStripMenuItem.Visible = false;

            //lblUser.Visible = false;
            userToolStripMenuItem1.Visible = false;
            loginToolStripMenuItem1.Visible = true;
            registerToolStripMenuItem2.Visible = true;

            viewUserToolStripMenuItem1.Visible = false;
            viewTopicToolStripMenuItem.Visible = false;
            helpToolStripMenuItem.Visible = false;

            backToolStripMenuItem.Visible = false;
            criteriaListToolStripMenuItem1.Visible = false;
            criteriaWeightToolStripMenuItem1.Visible = false;
            alternativeListToolStripMenuItem1.Visible = false;
            openAllFormToolStripMenuItem1.Visible = false;
            closeAllFormToolStripMenuItem1.Visible = false;
            resultToolStripMenuItem1.Visible = false;

            topicCountToolStripMenuItem.Visible = false;
            criteriaCountToolStripMenuItem.Visible = false;
            alternativeCountToolStripMenuItem.Visible = false;

            if (currentUser != null)
            {
                // SECOND PAGE, AFTER LOGIN
                //lblUser.Visible = true;
                //lblUser.Text = "Hi, " + currentUser.userName + "!";
                //lblUser.Parent = this;
                userToolStripMenuItem1.Visible = true;
                userToolStripMenuItem1.Text = "Hi, " + currentUser.userName + "!";

                loginToolStripMenuItem1.Visible = false;
                registerToolStripMenuItem2.Visible = false;
                
                if (currentUser.isAdmin)
                {
                    viewUserToolStripMenuItem1.Visible = true;
                }
                else
                {
                    viewUserToolStripMenuItem1.Visible = false;
                }
                viewTopicToolStripMenuItem.Visible = true;
                helpToolStripMenuItem.Visible = true;

                backToolStripMenuItem.Visible = false;
                criteriaListToolStripMenuItem1.Visible = false;
                criteriaWeightToolStripMenuItem1.Visible = false;
                alternativeListToolStripMenuItem1.Visible = false;
                openAllFormToolStripMenuItem1.Visible = false;
                closeAllFormToolStripMenuItem1.Visible = false;
                resultToolStripMenuItem1.Visible = false;

                topicCountToolStripMenuItem.Visible = true;

                if (currentUser.isAdmin)
                {
                    topicCountToolStripMenuItem.Text = "Topic(s): " + topicController.getTopicData("").Count;
                }
                else
                {
                    topicCountToolStripMenuItem.Text = "Topic(s): " + topicController.getTopicData(currentUser.userName).Count;
                }
                
                criteriaCountToolStripMenuItem.Visible = false;
                alternativeCountToolStripMenuItem.Visible = false;

                if (currentTopic != null)
                {
                    // THIRD PAGE, AFTER ACCESS TOPIC

                    loginToolStripMenuItem1.Visible = false;
                    registerToolStripMenuItem2.Visible = false;

                    viewUserToolStripMenuItem1.Visible = false;
                    viewTopicToolStripMenuItem.Visible = false;
                    helpToolStripMenuItem.Visible = true;

                    backToolStripMenuItem.Visible = true;
                    criteriaListToolStripMenuItem1.Visible = true;
                    closeAllFormToolStripMenuItem1.Visible = true;
                    resultToolStripMenuItem1.Visible = false;
                    
                    string topicId = currentTopic.topicId.ToString();
                    int countCriteria = mainController.countCriteria(topicId);
                    int countAlternative = alternativeListController.getAlternativeList(topicId).Count;

                    topicCountToolStripMenuItem.Visible = false;
                    criteriaCountToolStripMenuItem.Visible = true;
                    criteriaCountToolStripMenuItem.Text = "Criteria(s): " + countCriteria.ToString();
                    alternativeCountToolStripMenuItem.Visible = true;
                    alternativeCountToolStripMenuItem.Text = "Alternative(s): " + countAlternative.ToString();

                    if (countCriteria < 3 || countCriteria > 11)
                    {
                        criteriaWeightToolStripMenuItem1.Visible = false;
                        alternativeListToolStripMenuItem1.Visible = false;
                        openAllFormToolStripMenuItem1.Visible = false;
                        resultToolStripMenuItem1.Visible = false;
                    }
                    else
                    {
                        criteriaWeightToolStripMenuItem1.Visible = true;
                        alternativeListToolStripMenuItem1.Visible = true;
                        openAllFormToolStripMenuItem1.Visible = true;
                        resultToolStripMenuItem1.Visible = false;

                        if (countAlternative >= 2)
                        {
                            resultToolStripMenuItem1.Visible = true;
                        }
                    }
                }
            }
        }

        public void setCurrentTopic(Topic topic)
        {
            this.currentTopic = topic;
            
            this.Text = "Analytic Hierarchy Process: " + topic.topicName;
            
            updateTooltipVisibility();
        }

        public Topic getCurrentTopic()
        {
            return this.currentTopic;
        }

        public void setCurrentUser(User currentUser)
        {
            this.currentUser = currentUser;
        }

        public User getCurrentUser()
        {
            return this.currentUser;
        }

        public void openResultForm()
        {
            resultToolStripMenuItem1_Click(this, new EventArgs());
        }
        
        // MAINFORM EVENT
        private void MainMenu_SizeChanged(object sender, EventArgs e)
        {
            //if (this.WindowState == FormWindowState.Minimized ||
            //    this.WindowState == FormWindowState.Normal)
            //{
            //    this.WindowState = FormWindowState.Maximized;
            //}

            this.Refresh();
        }

        private void MainMenu_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (currentUser != null)
            {
                var mboxResponse = MessageBox.Show(this, "You are about to exit. Do you want to logout?",
                "Exit Application", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);

                if (mboxResponse == DialogResult.No)
                {
                    e.Cancel = true;
                }
            }
        }

        // TOOLSTRIP EVENT
        private void loadFileToolStripMenuItem_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.InitialDirectory = "C:\\";
            openFileDialog.RestoreDirectory = true;

            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                try
                {
                    MessageBox.Show("Saved!");
                }
                catch (Exception ex)
                {
                    MessageBox.Show(this, "Error: Could not load file.\nOriginal Error: " + ex.Message,
                        "File Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        private void saveFileToolStripMenuItem_Click(object sender, EventArgs e)
        {
            SaveFileDialog saveFileDialog = new SaveFileDialog();
            saveFileDialog.InitialDirectory = "C:\\";

            if (saveFileDialog.ShowDialog() == DialogResult.OK)
            {
                try
                {
                    MessageBox.Show("Saved!");
                }
                catch (Exception ex)
                {
                    MessageBox.Show(this, "Error: Could not save file.\nOriginal Error: " + ex.Message,
                        "File Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        public Form isFormOpened(Type FormType)
        {
            foreach (Form form in Application.OpenForms)
            {
                if (form.GetType() == FormType)
                    return form;
            }
            return null;
        }

        private void topicToolStripMenuItem_Click(object sender, EventArgs e)
        {
            TopicForm topicForm = null;
            if (isFormOpened(typeof(TopicForm)) == null)
            {
                topicForm = new TopicForm();
                topicForm.MdiParent = this;
                topicForm.Show();
            }
        }

        private void helpToolStripMenuItem_Click(object sender, EventArgs e)
        {
            HelpDialog helpDialog = null;
            if (isFormOpened(typeof(HelpDialog)) == null)
            {
                helpDialog = new HelpDialog();
                helpDialog.MdiParent = this;
                helpDialog.Show();
            }
        }

        private void backToolStripMenuItem_Click(object sender, EventArgs e)
        {
            var mboxResponse = MessageBox.Show(this, "Are you sure you want to back?\n(Unsaved work will not be saved)",
                "Back to Main Menu", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);

            if (mboxResponse == DialogResult.Yes)
            {
                closeAllChildrenFormExcept(typeof(HelpDialog), null);
                
                this.currentTopic = null;
                this.Text = "Analytic Hierarchy Process";
                updateTooltipVisibility();

                refreshAllChildrenForm();
            }
        }

        private void criteriaListToolStripMenuItem_Click(object sender, EventArgs e)
        {
            CriteriaForm criteriaForm = null;
            if (isFormOpened(typeof(CriteriaForm)) == null)
            {
                criteriaForm = new CriteriaForm();
                criteriaForm.MdiParent = this;
                criteriaForm.Show();
            }
            criteriaForm.BringToFront();
        }

        private void criteriaRankingToolStripMenuItem_Click(object sender, EventArgs e)
        {
            CriteriaRankingForm criteriaRankingForm = null;
            if (isFormOpened(typeof(CriteriaRankingForm)) == null)
            {
                criteriaRankingForm = new CriteriaRankingForm();
                criteriaRankingForm.MdiParent = this;
                criteriaRankingForm.Show();
            }
        }

        private AlternativeListForm alternativeListToolStripMenuItem_Click(object sender, EventArgs e)
        {
            AlternativeListForm alternativeListForm = null;
            if (isFormOpened(typeof(AlternativeListForm)) == null)
            {
                alternativeListForm = new AlternativeListForm();
                alternativeListForm.MdiParent = this;
                alternativeListForm.Show();
            }
            return alternativeListForm;
        }

        private void MainForm_Load(object sender, EventArgs e)
        {
            //mainController.dropAllTable();
            //MessageBox.Show("Hello, " + currentUser.userName + "!");

            //string userSession = mainController.checkSession();

            //if (userSession == "")
            //{
            //    currentUser = null;
            //}
            //else
            //{
            //    currentUser = new User(userSession);
            //}

            updateTooltipVisibility();
        }

        private void criteriaListToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            CriteriaForm criteriaForm = null;
            if (isFormOpened(typeof(CriteriaForm)) == null)
            {
                criteriaForm = new CriteriaForm();
                criteriaForm.MdiParent = this;
                criteriaForm.Show();
            }
        }

        private void criteriaWeightToolStripMenuItem_Click(object sender, EventArgs e)
        {
            CriteriaRankingForm criteriaRankingForm = null;
            if (isFormOpened(typeof(CriteriaRankingForm)) == null)
            {
                criteriaRankingForm = new CriteriaRankingForm();
                criteriaRankingForm.MdiParent = this;
                criteriaRankingForm.Show();
            }
        }

        private void alternativeListToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            AlternativeListForm alternativeListForm = null;
            if (isFormOpened(typeof(AlternativeListForm)) == null)
            {
                alternativeListForm = new AlternativeListForm();
                alternativeListForm.MdiParent = this;
                alternativeListForm.Show();
            }
        }

        private void openAllFormToolStripMenuItem_Click(object sender, EventArgs e)
        {
            // Close all opened form
            closeAllChildrenFormExcept(null, null);

            CriteriaForm criteriaForm = null;
            if (isFormOpened(typeof(CriteriaForm)) == null)
            {
                criteriaForm = new CriteriaForm();
                criteriaForm.MdiParent = this;

                criteriaForm.StartPosition = FormStartPosition.Manual;
                criteriaForm.Location = new Point(0, 0);
                criteriaForm.Show();
            }

            CriteriaRankingForm criteriaRankingForm = null;
            if (isFormOpened(typeof(CriteriaRankingForm)) == null)
            {
                criteriaRankingForm = new CriteriaRankingForm();
                criteriaRankingForm.MdiParent = this;

                criteriaRankingForm.StartPosition = FormStartPosition.Manual;
                criteriaRankingForm.Location = new Point(criteriaForm.Width, 0);
                criteriaRankingForm.Show();
            }

            AlternativeListForm alternativeListForm = null;
            if (isFormOpened(typeof(AlternativeListForm)) == null)
            {
                alternativeListForm = new AlternativeListForm();
                alternativeListForm.MdiParent = this;

                alternativeListForm.StartPosition = FormStartPosition.Manual;
                alternativeListForm.Location = new Point(0, criteriaForm.Height);
                alternativeListForm.Show();
            }

            int countAlternative = alternativeListController.getAlternativeList(currentTopic.topicId.ToString()).Count;
            ResultForm resultForm = null;
            if (isFormOpened(typeof(ResultForm)) == null && countAlternative >= 2)
            {
                resultForm = new ResultForm();
                resultForm.MdiParent = this;

                resultForm.StartPosition = FormStartPosition.Manual;
                resultForm.Location = new Point(alternativeListForm.Width, criteriaForm.Height);
                resultForm.Show();
            }
        }

        private void registerToolStripMenuItem2_Click(object sender, EventArgs e)
        {
            RegisterForm registerForm = null;
            if (isFormOpened(typeof(RegisterForm)) == null)
            {
                registerForm = new RegisterForm("Register", null);
                registerForm.MdiParent = this;
                registerForm.Show();
            }
        }

        public void loginToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            LoginForm loginForm = null;
            if (isFormOpened(typeof(LoginForm)) == null)
            {
                loginForm = new LoginForm();
                loginForm.MdiParent = this;
                loginForm.Show();
            }
        }

        private void closeAllFormToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            closeAllChildrenFormExcept(null, null);
        }

        private void resultToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            ResultForm resultForm = null;
            if (isFormOpened(typeof(ResultForm)) == null)
            {
                resultForm = new ResultForm();
                resultForm.MdiParent = this;
                resultForm.Show();
            }
        }

        private void changePasswordToolStripMenuItem_Click(object sender, EventArgs e)
        {
            ChangePasswordForm changePasswordForm = null;
            if (isFormOpened(typeof(ChangePasswordForm)) == null)
            {
                changePasswordForm = new ChangePasswordForm();
                changePasswordForm.MdiParent = this;
                changePasswordForm.Show();
            }
        }

        private void logoutToolStripMenuItem_Click(object sender, EventArgs e)
        {
            var mboxResponse = MessageBox.Show(this, "Are you sure you want to logout?",
                "Logout", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);

            if (mboxResponse == DialogResult.Yes)
            {
                closeAllChildrenFormExcept(null, null);

                this.currentUser = null;
                this.currentTopic = null;
                //mainController.deleteSession();
                updateTooltipVisibility();

                refreshAllChildrenForm();
            }
        }

        private void viewUserToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            ViewUserForm viewUserForm = null;
            if (isFormOpened(typeof(ViewUserForm)) == null)
            {
                viewUserForm = new ViewUserForm();
                viewUserForm.MdiParent = this;
                viewUserForm.Show();
            }
        }
    }
}
