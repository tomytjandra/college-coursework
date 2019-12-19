using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AHPApp
{
    public class Criteria
    {
        public int criteriaId { get; set; }
        public int topicId { get; set; }
        public string criteriaName { get; set; }
        public string criteriaUnit { get; set; }
        public bool isFewerBetter { get; set; }
        public bool isBoolean { get; set; }
    }
}
