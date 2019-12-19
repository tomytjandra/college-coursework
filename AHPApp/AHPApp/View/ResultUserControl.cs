using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace AHPApp
{
    public partial class ResultUserControl : UserControl
    {
        public ResultUserControl(int number, string alternativeName, double value)
        {
            InitializeComponent();

            lblNumber.Text = number.ToString() + ".";
            lblAlternative.Text = alternativeName.ToString();
            lblValue.Text = Math.Round(value * 100, 3).ToString() + "%"; 
        }

        private void ResultUserControl_Load(object sender, EventArgs e)
        {

        }

        private void lblValue_Click(object sender, EventArgs e)
        {

        }
    }
}
