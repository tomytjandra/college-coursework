﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using iTextSharp.text;
using iTextSharp.text.pdf;

namespace AHPApp
{
    public class TwoColumnHeaderFooter : PdfPageEventHelper
    {
        private string currentUserName;

        // This is the contentbyte object of the writer
        PdfContentByte cb;
        // we will put the final number of pages in a template
        PdfTemplate template;
        // this is the BaseFont we are going to use for the header / footer
        BaseFont bfBold = null;
        BaseFont bfNormal = null;
        BaseFont bfItalic = null;
        // This keeps track of the creation time
        DateTime PrintTime = DateTime.Now;
        #region Properties
        private string _Title;
        public string Title
        {
            get { return _Title; }
            set { _Title = value; }
        }

        private string _HeaderLeft;
        public string HeaderLeft
        {
            get { return _HeaderLeft; }
            set { _HeaderLeft = value; }
        }
        private string _HeaderRight;
        public string HeaderRight
        {
            get { return _HeaderRight; }
            set { _HeaderRight = value; }
        }
        private Font _HeaderFont;
        public Font HeaderFont
        {
            get { return _HeaderFont; }
            set { _HeaderFont = value; }
        }
        private Font _FooterFont;
        public Font FooterFont
        {
            get { return _FooterFont; }
            set { _FooterFont = value; }
        }
        #endregion

        public TwoColumnHeaderFooter(string currentUserName)
        {
            this.currentUserName = currentUserName;
        }

        // we override the onOpenDocument method
        public override void OnOpenDocument(PdfWriter writer, Document document)
        {
            try
            {
                PrintTime = DateTime.Now;
                bfBold = BaseFont.CreateFont(BaseFont.HELVETICA_BOLD, BaseFont.CP1252, BaseFont.NOT_EMBEDDED);
                bfNormal = BaseFont.CreateFont(BaseFont.HELVETICA, BaseFont.CP1252, BaseFont.NOT_EMBEDDED);
                bfItalic = BaseFont.CreateFont(BaseFont.HELVETICA_OBLIQUE, BaseFont.CP1252, BaseFont.NOT_EMBEDDED);
                cb = writer.DirectContent;
                template = cb.CreateTemplate(50, 50);
            }
            catch (DocumentException de)
            {
            }
            catch (System.IO.IOException ioe)
            {
            }
        }

        public override void OnStartPage(PdfWriter writer, Document document)
        {
            base.OnStartPage(writer, document);
            Rectangle pageSize = document.PageSize;
            if (Title != string.Empty)
            {
                cb.BeginText();
                cb.SetFontAndSize(bfBold, 15);
                cb.SetRGBColorFill(0, 0, 0);
                cb.SetTextMatrix(pageSize.GetLeft(40), pageSize.GetTop(40));
                cb.ShowText(Title);
                cb.EndText();
            }
            if (HeaderLeft + HeaderRight != string.Empty)
            {
                cb.BeginText();
                cb.SetFontAndSize(bfItalic, 12);
                cb.SetRGBColorFill(0, 0, 0);
                cb.SetTextMatrix(pageSize.GetLeft(40), pageSize.GetTop(60));
                cb.ShowText(HeaderLeft + ": " + HeaderRight);
                cb.EndText();
            }

            //if (HeaderLeft + HeaderRight != string.Empty)
            //{
            //    PdfPTable HeaderTable = new PdfPTable(2);
            //    HeaderTable.DefaultCell.VerticalAlignment = Element.ALIGN_MIDDLE;
            //    HeaderTable.TotalWidth = pageSize.Width - 80;
            //    HeaderTable.SetWidthPercentage(new float[] { 50, 120 + HeaderRight.Length }, pageSize);

                //    PdfPCell HeaderLeftCell = new PdfPCell(new Phrase(8, HeaderLeft));
                //    HeaderLeftCell.Padding = 5;
                //    HeaderLeftCell.PaddingBottom = 8;
                //    HeaderLeftCell.BorderWidthRight = 0;
                //    HeaderTable.AddCell(HeaderLeftCell);
                //    PdfPCell HeaderRightCell = new PdfPCell(new Phrase(8, HeaderRight));
                //    HeaderRightCell.HorizontalAlignment = PdfPCell.ALIGN_LEFT;
                //    HeaderRightCell.Padding = 5;
                //    HeaderRightCell.PaddingBottom = 8;
                //    HeaderRightCell.BorderWidthLeft = 0;
                //    HeaderTable.AddCell(HeaderRightCell);
                //    cb.SetRGBColorFill(0, 0, 0);
                //    HeaderTable.WriteSelectedRows(0, -1, pageSize.GetLeft(40), pageSize.GetTop(50), cb);
                //}
        }
        public override void OnEndPage(PdfWriter writer, Document document)
        {
            base.OnEndPage(writer, document);
            int pageN = writer.PageNumber;
            String text = "Page " + pageN + " of ";
            float len = bfItalic.GetWidthPoint(text, 8);
            Rectangle pageSize = document.PageSize;
            cb.SetRGBColorFill(100, 100, 100);

            cb.BeginText();
            cb.SetFontAndSize(iTextSharp.text.pdf.BaseFont.CreateFont(iTextSharp.text.pdf.BaseFont.HELVETICA_BOLDOBLIQUE, iTextSharp.text.pdf.BaseFont.CP1252, iTextSharp.text.pdf.BaseFont.EMBEDDED), 8);
            cb.SetTextMatrix(pageSize.GetLeft(40), pageSize.GetBottom(30));
            cb.ShowText("Generated automatically at " + PrintTime.ToString() + " by " + currentUserName);
            cb.EndText();
            cb.AddTemplate(template, pageSize.GetLeft(40) + len, pageSize.GetBottom(30));

            //cb.BeginText();
            //cb.SetFontAndSize(bf, 8);
            //cb.ShowTextAligned(PdfContentByte.ALIGN_RIGHT,
            //text,
            //pageSize.GetRight(40),
            //pageSize.GetBottom(30), 0);
            //cb.EndText();
        }
        public override void OnCloseDocument(PdfWriter writer, Document document)
        {
            base.OnCloseDocument(writer, document);
            //template.BeginText();
            //template.SetFontAndSize(bf, 8);
            //template.SetTextMatrix(0, 0);
            //template.ShowText("" + (writer.PageNumber));
            //template.EndText();
        }
    }
}
