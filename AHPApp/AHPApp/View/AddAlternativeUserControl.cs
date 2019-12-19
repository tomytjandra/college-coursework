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
    public partial class AddAlternativeUserControl : UserControl
    {
        private int criteriaId;
        private bool isBoolean;

        public AddAlternativeUserControl(int criteriaId, string criteriaName, string criteriaUnit, bool isBoolean, double value)
        {
            InitializeComponent();

            numericUpDown1.Maximum = Decimal.MaxValue;
            numericUpDown1.Minimum = 0;

            this.criteriaId = criteriaId;
            lblCriteriaName.Text = criteriaName;
            lblCriteriaUnit.Text = criteriaUnit;
            this.isBoolean = isBoolean;

            if (isBoolean)
            {
                checkBox1.Visible = true;
                numericUpDown1.Visible = false;
                if (value == 0)
                {
                    checkBox1.Checked = false;
                }
                else
                {
                    checkBox1.Checked = true;
                }
            }
            else
            {
                checkBox1.Visible = false;
                numericUpDown1.Visible = true;
                try
                {
                    numericUpDown1.Value = (decimal)value;
                }
                catch
                {
                    numericUpDown1.Value = numericUpDown1.Minimum;
                }
            }
        }
        
        public Criteria getCriteria()
        {
            Criteria criteria = new Criteria();
            criteria.criteriaId = this.criteriaId;
            criteria.criteriaName = lblCriteriaName.Text;
            criteria.criteriaUnit = lblCriteriaUnit.Text;
            criteria.isBoolean = this.isBoolean;
            return criteria;
        }

        public double getValue()
        {
            double value;

            if (isBoolean)
            {
                if (checkBox1.Checked)
                {
                    value = 1;
                }
                else
                {
                    value = 0;
                }
            }
            else
            {
                value = (double) numericUpDown1.Value;
            }

            return value;
        }

        public void setValue2Default()
        {
            if (isBoolean)
            {
                checkBox1.Checked = false;
            }
            else
            {
                numericUpDown1.Value = numericUpDown1.Minimum;
            }
        }

        private void AddAlternativeUserControl_Load(object sender, EventArgs e)
        {

        }

        private void lblCriteriaUnit_Click(object sender, EventArgs e)
        {

        }

        private void numericUpDown1_ValueChanged(object sender, EventArgs e)
        {

        }

        private void numericUpDown1_KeyDown(object sender, KeyEventArgs e)
        {
            AddAlternativeForm addAlternativeForm = (AddAlternativeForm)this.ParentForm;
            addAlternativeForm.txtAlternativeName_KeyDown(this, e);
        }
    }
}
