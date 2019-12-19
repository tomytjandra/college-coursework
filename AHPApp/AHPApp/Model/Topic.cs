using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AHPApp
{
    public class Topic
    {
        public int topicId { get; set; }
        public string topicName { get; set; }

        public Topic(int topicId, string topicName)
        {
            this.topicId = topicId;
            this.topicName = topicName;
        }
    }
}
