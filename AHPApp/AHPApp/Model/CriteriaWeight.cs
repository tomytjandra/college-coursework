using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AHPApp
{
    public class CriteriaWeight
    {
        public int criteriaWeightId { get; set; }
        public int criteria1Id { get; set; }
        public int criteria2Id { get; set; }
        public double importanceLevel { get; set; }

        public string criteria1Name { get; set; }
        public string criteria2Name { get; set; }
    }
}
