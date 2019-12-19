using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using iTextSharp.text;
using iTextSharp.text.pdf;
using System.Net.Http.Headers;
using System.Windows.Forms.DataVisualization.Charting;

namespace AHPApp
{
    public partial class ResultForm : Form
    {
        private MainForm mainForm;
        private CriteriaController criteriaController;
        private AlternativeListController alternativeListController;
        private ResultController resultController;
        private DataView data;
        string currentTopicId;

        public ResultForm()
        {
            InitializeComponent();
        }

        public override void Refresh()
        {
            ResultForm_Load(this, new EventArgs());
            base.Refresh();
        }

        private void ResultForm_Load(object sender, EventArgs e)
        {
            mainForm = (MainForm)this.MdiParent;
            criteriaController = new CriteriaController();
            alternativeListController = new AlternativeListController();
            resultController = new ResultController();
            currentTopicId = mainForm.getCurrentTopic().topicId.ToString();

            this.Text = "Result for " + mainForm.getCurrentTopic().topicName;

            if (alternativeListController.getAlternativeList(currentTopicId).Count < 2)
            {
                this.Close();
            }
            else
            {
                loadDynamicUI();
            }
        }

        public Dictionary<string, double> relativeResult(Dictionary<string, double> result)
        {
            double min = result.ElementAt(0).Value;
            double max = result.ElementAt(0).Value;
            foreach (var res in result)
            {
                if (res.Value < min)
                {
                    min = res.Value;
                }

                if (res.Value > max)
                {
                    max = res.Value;
                }
            }
            
            Dictionary<string, double> relativeResult = new Dictionary<string, double>();
            double range = max - min;
            foreach (var res in result)
            {
                relativeResult.Add(res.Key, (max - res.Value) / range);
            }

            return relativeResult;
        }

        public void loadGraph(Dictionary<string, double> result)
        {
            // clear plot
            chart1.Titles.Clear();
            foreach (var series in chart1.Series)
            {
                series.Points.Clear();
            }

            // re-plot
            //chart1.Titles.Add("Topic: " + mainForm.getCurrentTopic().topicName);
            chart1.ChartAreas[0].AxisX.Title = "Alternative";
            chart1.ChartAreas[0].AxisY.Title = "Probability";
            chart1.ChartAreas[0].AxisX.MajorGrid.LineWidth = 0;
            chart1.ChartAreas[0].AxisY.MajorGrid.LineWidth = 0;

            for (int i = 0; i < result.Count; i++)
            {
                chart1.Series["Alternatives"].Points.AddXY(result.ElementAt(i).Key, result.ElementAt(i).Value);
                chart1.Series["Alternatives"].Points[i].Label = Math.Round(result.ElementAt(i).Value * 100, 3).ToString() + "%";
                chart1.Series["Alternatives"].Points[i].LabelForeColor = Color.Black;
                chart1.Series["Alternatives"].Points[i].Font = new System.Drawing.Font("Trebuchet MS", 8, System.Drawing.FontStyle.Bold);
            }
        }

        public void loadDynamicUI()
        {
            flowLayoutPanel1.Controls.Clear();
            Dictionary<string, double> finalResult = resultController.finalResult(currentTopicId);
                       
            for (int i = 0; i < finalResult.Count; i++)
            {
                string alternativeName = finalResult.Keys.ElementAt(i);
                double value = finalResult.Values.ElementAt(i);

                ResultUserControl resultUserControl = new ResultUserControl(i+1, alternativeName, value);
                resultUserControl.Parent = flowLayoutPanel1;
                flowLayoutPanel1.Controls.Add(resultUserControl);
            }

            loadGraph(finalResult);
        }

        private void btnExport_Click(object sender, EventArgs e)
        {
            saveFileDialog1.Title = "Export to PDF";
            saveFileDialog1.Filter = "(*.pdf)|*.pdf";
            saveFileDialog1.InitialDirectory = @"D:\";
            saveFileDialog1.FileName = "AHP_" + mainForm.getCurrentTopic().topicName + "_" + mainForm.getCurrentUser().userName;
            saveFileDialog1.FileOk += saveFileDialog1_FileOk;

            if (saveFileDialog1.ShowDialog() == DialogResult.OK)
            {
                try
                {
                    iTextSharp.text.Document doc = new iTextSharp.text.Document();
                    PdfWriter pdfWriter = PdfWriter.GetInstance(doc, new FileStream(saveFileDialog1.FileName, FileMode.Create));
                    //pdfWriter.PageEvent = new ITextEvents(mainForm.getCurrentTopic().topicName.ToUpper());
                    
                    // FONT DEFINITION
                    //iTextSharp.text.pdf.BaseFont bfTitle = iTextSharp.text.pdf.BaseFont.CreateFont(iTextSharp.text.pdf.BaseFont.HELVETICA_BOLD, iTextSharp.text.pdf.BaseFont.CP1252, iTextSharp.text.pdf.BaseFont.EMBEDDED);
                    //iTextSharp.text.Font fontTitle = new iTextSharp.text.Font(bfTitle, 15);
                    //fontTitle.SetStyle(iTextSharp.text.Font.UNDERLINE);
                    iTextSharp.text.pdf.BaseFont bfNormal = iTextSharp.text.pdf.BaseFont.CreateFont(iTextSharp.text.pdf.BaseFont.HELVETICA, iTextSharp.text.pdf.BaseFont.CP1252, iTextSharp.text.pdf.BaseFont.EMBEDDED);
                    iTextSharp.text.pdf.BaseFont bfBold = iTextSharp.text.pdf.BaseFont.CreateFont(iTextSharp.text.pdf.BaseFont.HELVETICA_BOLD, iTextSharp.text.pdf.BaseFont.CP1252, iTextSharp.text.pdf.BaseFont.EMBEDDED);
                    iTextSharp.text.Font fontSubtitle = new iTextSharp.text.Font(bfBold, 13);
                    iTextSharp.text.Font fontColHeader = new iTextSharp.text.Font(bfBold, 11);
                    iTextSharp.text.Font fontTable = new iTextSharp.text.Font(bfNormal, 10);
                    iTextSharp.text.Font fontConclusion = new iTextSharp.text.Font(bfNormal, 10);
                    fontConclusion.SetStyle(iTextSharp.text.Font.UNDERLINE);

                    // HEADER AND FOOTER
                    TwoColumnHeaderFooter PageEventHandler = new TwoColumnHeaderFooter(mainForm.getCurrentUser().userName);
                    pdfWriter.PageEvent = PageEventHandler;
                    PageEventHandler.Title = "AHP RESULT";
                    PageEventHandler.HeaderFont = FontFactory.GetFont(BaseFont.COURIER_BOLD, 10, iTextSharp.text.Font.BOLD);
                    PageEventHandler.HeaderLeft = "Topic";
                    PageEventHandler.HeaderRight = mainForm.getCurrentTopic().topicName.ToUpper();
                    
                    doc.Open();
                    
                    // TITLE
                    //Paragraph title = new Paragraph(mainForm.getCurrentTopic().topicName.ToUpper(), fontTitle);
                    //title.Alignment = Element.ALIGN_CENTER;
                    //doc.Add(title);

                    doc.Add(new Paragraph(" "));
                    // SUBTITLE: DETAIL ALTERNATIVE
                    Paragraph subtitle1 = new Paragraph("DETAIL ALTERNATIVE", fontSubtitle);
                    subtitle1.Alignment = Element.ALIGN_CENTER;
                    subtitle1.SpacingBefore = 25;
                    subtitle1.SpacingAfter = 20;
                    doc.Add(subtitle1);

                    // TABLE DETAIL
                    bool switchCloseAlternativeListForm = true;
                    AlternativeListForm alternativeListForm = null;
                    if (mainForm.isFormOpened(typeof(AlternativeListForm)) != null)
                    {
                        switchCloseAlternativeListForm = false;
                        alternativeListForm = (AlternativeListForm) mainForm.isFormOpened(typeof(AlternativeListForm));
                        alternativeListForm.MdiParent = mainForm;
                        alternativeListForm.Show();
                    }
                    else
                    {
                        alternativeListForm = mainForm.getAlternativeListForm();
                    }

                    DataGridView dataGridView = alternativeListForm.getDGV();
                    
                    PdfPTable pdfPTable = new PdfPTable(dataGridView.ColumnCount);
                        // Header Column
                    foreach (DataGridViewColumn column in dataGridView.Columns)
                    {
                        PdfPCell cell = new PdfPCell(new Phrase(column.HeaderText, fontColHeader));
                        //cell.BackgroundColor = new iTextSharp.text.Color(240, 240, 240);
                        cell.HorizontalAlignment = Element.ALIGN_CENTER;
                        cell.VerticalAlignment = Element.ALIGN_MIDDLE;
                        pdfPTable.AddCell(cell);
                    }
                        // Adding DataRow
                    foreach (DataGridViewRow row in dataGridView.Rows)
                    {
                        foreach (DataGridViewCell cell in row.Cells)
                        {
                            PdfPCell pdfPCell = new PdfPCell(new Phrase(cell.Value.ToString(), fontTable));
                            pdfPCell.HorizontalAlignment = Element.ALIGN_CENTER;
                            pdfPCell.VerticalAlignment = Element.ALIGN_MIDDLE;
                            pdfPTable.AddCell(pdfPCell);
                        }
                    }
                    doc.Add(pdfPTable);

                    mainForm.refreshAllChildrenForm();
                    if (switchCloseAlternativeListForm)
                    {
                        alternativeListForm.Close();
                    }

                    // SUBTITLE: COMPARISON
                    Paragraph subtitle2 = new Paragraph("COMPARISON", fontSubtitle);
                    subtitle2.Alignment = Element.ALIGN_CENTER;
                    subtitle2.SpacingBefore = 25;
                    doc.Add(subtitle2);

                    // CHART IMAGE
                    MemoryStream ms = new MemoryStream();
                    chart1.SaveImage(ms, ChartImageFormat.Png);
                    iTextSharp.text.Image chart_img = iTextSharp.text.Image.GetInstance(ms.ToArray());
                    chart_img.SetDpi(300, 300);
                    chart_img.ScaleToFit(300f, 300f);
                    chart_img.Alignment = Element.ALIGN_CENTER;
                    doc.Add(chart_img);

                    // SUBTITLE: CONCLUSION
                    Paragraph subtitle3 = new Paragraph("CONCLUSION", fontSubtitle);
                    subtitle3.Alignment = Element.ALIGN_CENTER;
                    subtitle3.SpacingBefore = 25;
                    doc.Add(subtitle3);

                    // CONCLUSION
                    List<List<string>> conclusion = resultController.conclusionBestWorst(currentTopicId);
                    
                    if (conclusion == null)
                    {
                        doc.Add(new Paragraph("Cannot conclude anything, since the data is all the same.", fontTable));
                    }
                    else
                    {
                        // SUB SUBTITLE BEST ALTERNATIVE
                        Paragraph subtitleBest = new Paragraph("Best Alternative(s)", fontConclusion);
                        subtitleBest.SpacingBefore = 10;
                        subtitleBest.SpacingAfter = 5;
                        subtitleBest.Alignment = Element.ALIGN_CENTER;
                        doc.Add(subtitleBest);

                        int numbering = 1;
                        foreach (List<string> conc in conclusion)
                        {
                            if (conc[0] == "Best")
                            {
                                string oneLine = /*numbering + ". " +*/ conc[1] + " (Best criteria: ";
                                foreach (string crit in resultController.bestWorstCriteria(currentTopicId, conc))
                                {
                                    oneLine += crit + ", ";
                                }

                                Paragraph text = new Paragraph(oneLine.Substring(0, oneLine.Length - 2) + ")\n", fontTable);
                                text.Alignment = Element.ALIGN_CENTER;
                                doc.Add(text);
                                numbering++;
                            }
                        }

                        // SUB SUBTITLE WORST ALTERNATIVE
                        Paragraph subtitleWorst = new Paragraph("Worst Alternative(s)", fontConclusion);
                        subtitleWorst.SpacingBefore = 10;
                        subtitleWorst.SpacingAfter = 5;
                        subtitleWorst.Alignment = Element.ALIGN_CENTER;
                        doc.Add(subtitleWorst);
                        
                        numbering = 1;
                        foreach (List<string> conc in conclusion)
                        {
                            if (conc[0] == "Worst")
                            {
                                string oneLine = /*numbering + ". " +*/ conc[1] + " (Worst criteria: ";
                                foreach (string crit in resultController.bestWorstCriteria(currentTopicId, conc))
                                {
                                    oneLine += crit + ", ";
                                }

                                Paragraph text = new Paragraph(oneLine.Substring(0, oneLine.Length - 2) + ")\n", fontTable);
                                text.Alignment = Element.ALIGN_CENTER;
                                doc.Add(text);
                                numbering++;
                            }
                        }
                    }
                    
                    doc.Close();

                    // DIALOG
                    int start = saveFileDialog1.FileName.LastIndexOf('\\') + 1;
                    int length = saveFileDialog1.FileName.Length;
                    
                    var mboxResponse = MessageBox.Show(this, "Successfully exported \"" + saveFileDialog1.FileName.Substring(start, length-start) + "\" to\n" + saveFileDialog1.FileName.Substring(0, start) + "\nDo you want to open the file?", "Export to PDF", MessageBoxButtons.YesNo, MessageBoxIcon.Information);

                    if (mboxResponse == DialogResult.Yes)
                    {
                        System.Diagnostics.Process.Start(saveFileDialog1.FileName);
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show(this, "An error occured:\n" + ex.Message, "Export to PDF", MessageBoxButtons.OK, MessageBoxIcon.Hand);
                }
            }
        }

        private void saveFileDialog1_FileOk(object sender, CancelEventArgs e)
        {
        }

        private void button1_Click(object sender, EventArgs e)
        {
            List<List<string>> conclusion = resultController.conclusionBestWorst(currentTopicId);

            foreach (List<string> temp in conclusion)
            {
                string bestWorst = temp[0];
                string alternativeName = temp[1];

                foreach (string crit in resultController.bestWorstCriteria(currentTopicId, temp))
                {
                    MessageBox.Show(bestWorst + " " + alternativeName + " " + crit);
                }
            }
        }
    }
}