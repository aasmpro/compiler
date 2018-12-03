using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace compiler
{
    public static class LexicalAnalysis
    {
        public static string keywords = " auto break case char const continue default do double else enum extern float for goto if int long register return short signed sizeof static struct switch typedef union unsigned void volatile while ";
        public static string digits = "0123456789";
        public static string letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_";
        public static string punctuations = "{}()[];,.";
        public static string signs = "+-/*=!<>&|";
        public static string strings = "\"";
        public static string delimiters = "\t\n ";
        public static string all = digits + letters + punctuations + signs + strings + delimiters;

        public static string state = "ST0";
        public static string stream = "";
        public static string identifiers = "";

        private static void PrintUngetch(char ch)
        {
            if (!delimiters.Contains(ch))
            {
                Console.WriteLine("ungetch");
            }
        }
        private static void PrintError()
        {
            Console.WriteLine("Error");
            stream = "";
        }
        private static void PrintNum(string type)
        {
            Console.WriteLine("{0}\t{1}", stream, type);
            stream = "";
        }
        private static void PrintStr()
        {
            Console.WriteLine("{0}\tSTR", stream);
            stream = "";
        }
        private static void PrintPunctuatuin(Char type)
        {
            Console.WriteLine("{0}\tPUNCTUATION", type);
            stream = "";
        }
        private static void PrintIdentifier()
        {
            Console.WriteLine("{0}\tIDENTIFIER", stream);
            if (identifiers.Contains(stream))
            {
                Console.WriteLine("false");
            }
            else
            {
                identifiers += stream + " ";
                Console.WriteLine("true");
            }
            stream = "";
        }
        private static void PrintOperator(string type)
        {
            Console.WriteLine("{0}\t{1}", stream, type);
            stream = "";
        }
        private static void PrintKeyword()
        {
            Console.WriteLine("{0}\tKEYWORD", stream);
            stream = "";
        }

        public static void SetState(char ch)
        {
            switch (state){
                case "ST0": ST0(ch); break;

                case "NUM1": NUM1(ch); break;
                case "NUM2": NUM2(ch); break;
                case "NUM3": NUM3(ch); break;
                case "NUM4": NUM4(ch); break;
                case "NUM5": NUM5(ch); break;
                case "NUM6": NUM6(ch); break;

                case "OPP": OPP(ch); break;
                case "OPS": OPS(ch); break;
                case "OPM": OPM(ch); break;
                case "OPA": OPA(ch); break;
                case "OPN": OPN(ch); break;
                case "OPL": OPL(ch); break;
                case "OPG": OPG(ch); break;
                case "OPZ": OPZ(ch); break;
                case "OPX": OPX(ch); break;
                    
                case "OPD1": OPD1(ch); break;
                case "OPD2": OPD2(ch); break;
                case "OPD3": OPD3(ch); break;
                case "OPD4": OPD4(ch); break;

                case "STR": STR(ch); break;
                case "ID": ID(ch); break;

                case "OTH": OTH(ch); break;
            }
        }

        private static void ST0(char ch)
        {
            if (digits.Contains(ch)) { state = "NUM1"; stream += ch; }
            else if (letters.Contains(ch)) { state = "ID"; stream += ch; }
            else if (punctuations.Contains(ch)) { PrintPunctuatuin(ch); }
            else if (delimiters.Contains(ch)) { }
            else if (ch == '"') { state = "STR"; stream += ch; }
            else if (ch == '+') { state = "OPP"; stream += ch; }
            else if (ch == '-') { state = "OPS"; stream += ch; }
            else if (ch == '*') { state = "OPM"; stream += ch; }
            else if (ch == '=') { state = "OPA"; stream += ch; }
            else if (ch == '!') { state = "OPN"; stream += ch; }
            else if (ch == '<') { state = "OPL"; stream += ch; }
            else if (ch == '>') { state = "OPG"; stream += ch; }
            else if (ch == '&') { state = "OPZ"; stream += ch; }
            else if (ch == '|') { state = "OPX"; stream += ch; }
            else if (ch == '/') { state = "OPD1"; stream += ch; }
            else { state = "OTH"; stream += ch; }
        }

        private static void NUM1(char ch)
        {
            if (digits.Contains(ch)) { stream += ch; }
            else if(ch == '.') { state = "NUM2"; stream += ch; }
            else if(ch == 'e' || ch == 'E') { state = "NUM4"; stream += ch; }
            else {
                PrintNum("INT");
                PrintUngetch(ch);
                state = "ST0";
                SetState(ch);
            }
        }
        private static void NUM2(char ch)
        {
            if (digits.Contains(ch)) { state = "NUM3"; stream += ch; }
            else
            {
                PrintError();
                PrintUngetch(ch);
                state = "ST0";
                SetState(ch);
            }
        }
        private static void NUM3(char ch)
        {
            if (digits.Contains(ch)) { stream += ch; }
            else if (ch == 'e' || ch == 'E') { state = "NUM4"; stream += ch; }
            else
            {
                PrintNum("REAL");
                PrintUngetch(ch);
                state = "ST0";
                SetState(ch);
            }
        }
        private static void NUM4(char ch)
        {
            if (digits.Contains(ch)) { state = "NUM6"; stream += ch; }
            else if (ch == '+' || ch == '-') { state = "NUM5"; stream += ch; }
            else
            {
                PrintError();
                PrintUngetch(ch);
                state = "ST0";
                SetState(ch);
            }
        }
        private static void NUM5(char ch)
        {
            if (digits.Contains(ch)) { state = "NUM6"; stream += ch; }
            else
            {
                PrintError();
                PrintUngetch(ch);
                state = "ST0";
                SetState(ch);
            }
        }
        private static void NUM6(char ch)
        {
            if (digits.Contains(ch)) { stream += ch; }
            else
            {
                PrintNum("SCI");
                PrintUngetch(ch);
                state = "ST0";
                SetState(ch);
            }
        }

        private static void OPP(char ch)
        {
            if (ch == '+') {
                stream += ch;
                PrintOperator("INC");
                state = "ST0";
            }
            else if (ch == '=')
            {
                stream += ch;
                PrintOperator("ADD_ASSIGN");
                state = "ST0";
            }
            else
            {
                PrintOperator("ADD");
                PrintUngetch(ch);
                state = "ST0";
                SetState(ch);
            }
        }
        private static void OPS(char ch)
        {
            if (ch == '-')
            {
                stream += ch;
                PrintOperator("DEC");
                state = "ST0";
            }
            else if (ch == '=')
            {
                stream += ch;
                PrintOperator("SUB_ASSIGN");
                state = "ST0";
            }
            else
            {
                PrintOperator("SUB");
                PrintUngetch(ch);
                state = "ST0";
                SetState(ch);
            }
        }
        private static void OPM(char ch)
        {
            if (ch == '=')
            {
                stream += ch;
                PrintOperator("MUL_ASSIGN");
                state = "ST0";
            }
            else
            {
                PrintOperator("MUL");
                PrintUngetch(ch);
                state = "ST0";
                SetState(ch);
            }
        }
        private static void OPA(char ch)
        {
            if (ch == '=')
            {
                stream += ch;
                PrintOperator("EQ");
                state = "ST0";
            }
            else
            {
                PrintOperator("ASSIGN");
                PrintUngetch(ch);
                state = "ST0";
                SetState(ch);
            }
        }
        private static void OPN(char ch)
        {
            if (ch == '=')
            {
                stream += ch;
                PrintOperator("NE");
                state = "ST0";
            }
            else
            {
                PrintOperator("NOT");
                PrintUngetch(ch);
                state = "ST0";
                SetState(ch);
            }
        }
        private static void OPG(char ch)
        {
            if (ch == '=')
            {
                stream += ch;
                PrintOperator("GE");
                state = "ST0";
            }
            else
            {
                PrintOperator("GT");
                PrintUngetch(ch);
                state = "ST0";
                SetState(ch);
            }
        }
        private static void OPL(char ch)
        {
            if (ch == '=')
            {
                stream += ch;
                PrintOperator("LE");
                state = "ST0";
            }
            else
            {
                PrintOperator("LT");
                PrintUngetch(ch);
                state = "ST0";
                SetState(ch);
            }
        }
        private static void OPZ(char ch)
        {
            if (ch == '&')
            {
                stream += ch;
                PrintOperator("AND");
                state = "ST0";
            }
            else
            {
                PrintError();
                PrintUngetch(ch);
                state = "ST0";
                SetState(ch);
            }
        }
        private static void OPX(char ch)
        {
            if (ch == '|')
            {
                stream += ch;
                PrintOperator("OR");
                state = "ST0";
            }
            else
            {
                PrintError();
                PrintUngetch(ch);
                state = "ST0";
                SetState(ch);
            }
        }

        private static void OPD1(char ch)
        {
            if (ch == '=')
            {
                stream += ch;
                PrintOperator("DIV_ASSIGN");
                state = "ST0";
            }
            else if (ch == '*')
            {
                stream += ch;
                state = "OPD2";
            }
            else if (ch == '/')
            {
                stream += ch;
                state = "OPD4";
            }
            else
            {
                PrintOperator("DIV");
                PrintUngetch(ch);
                state = "ST0";
                SetState(ch);
            }
        }
        private static void OPD2(char ch)
        {
            if (ch == '*')
            {
                stream += ch;
                state = "OPD3";
            }
            else
            {
                stream += ch;
            }
        }
        private static void OPD3(char ch)
        {
            if (ch == '/')
            {
                stream = "";
                state = "ST0";
            }
            else if (ch == '*')
            {
                stream += ch;
            }
            else
            {
                stream += ch;
                state = "OPD2";
            }
        }
        private static void OPD4(char ch)
        {
            if (ch == '\n')
            {
                stream = "";
                state = "ST0";
            }
            else
            {
                stream += ch;
            }
        }

        private static void STR(char ch)
        {
            if (ch == '\"')
            {
                stream += ch;
                PrintStr();
                state = "ST0";
            }
            else
            {
                stream += ch;
            }
        }
        private static void ID(char ch)
        {
            if (letters.Contains(ch) || digits.Contains(ch))
            {
                stream += ch;
            }
            else
            {
                if (keywords.Contains(" "+ stream + " "))
                {
                    PrintKeyword();
                }
                else
                {
                    PrintIdentifier();
                }
                PrintUngetch(ch);
                state = "ST0";
                SetState(ch);
            }
        }

        private static void OTH(char ch)
        {
            if (all.Contains(ch))
            {
                PrintError();
                state = "ST0";
                SetState(ch);
            }
            else
            {
                stream += ch;
            }
        }
    }
}
