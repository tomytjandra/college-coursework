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
    public partial class DeleteConfirmation : Form
    {
        public DeleteConfirmation(string dataToBeDeleted, string dataValue)
        {
            InitializeComponent();
            this.Text = this.Text + " " + dataToBeDeleted + ": " + dataValue;
            pbIcon.Image = Bitmap.FromHicon(SystemIcons.Warning.Handle);
            lblWarning.Text = "This action will delete the entire data of this " + dataToBeDeleted.ToLower() + ".\nEnter the captcha below if you are agree.";
            lblCaptcha.Text = generateCaptcha();
        }

        public string generateCaptcha()
        {
            string captcha = "";
            Random random = new Random();

            for (int i=0; i<6; i++)
            {
                captcha += Convert.ToChar(random.Next(65, 91));
            }

            return captcha;
        }

        private void btnResetCaptcha_Click(object sender, EventArgs e)
        {
            lblCaptcha.Text = generateCaptcha();
        }

        private void btnConfirmDelete_Click(object sender, EventArgs e)
        {
            string captcha = lblCaptcha.Text;
            string captchaInput = txtCaptcha.Text;

            if (captchaInput.ToUpper() != captcha.ToUpper())
            {
                lblCaptcha.Text = generateCaptcha();
                txtCaptcha.Text = "WRONG CAPTCHA!";
                txtCaptcha.ForeColor = Color.White;
                txtCaptcha.BackColor = Color.Red;
            }
            else
            {
                this.DialogResult = DialogResult.OK;
                this.Close();
            }
        }

        private void txtCaptcha_MouseEnter(object sender, EventArgs e)
        {
            if (txtCaptcha.Text == "WRONG CAPTCHA!")
            {
                txtCaptcha.Text = "";
                txtCaptcha.ForeColor = Color.Black;
                txtCaptcha.BackColor = Color.White;
            }
        }
    }
}
