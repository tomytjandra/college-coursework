using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SQLite;

namespace AHPApp
{
    class ResultController
    {
        static MainController mainController = new MainController();
        AlternativeListController alternativeListController = new AlternativeListController();
        CriteriaController criteriaController = new CriteriaController();
        CriteriaWeightController criteriaWeightController = new CriteriaWeightController();
        SQLiteConnection conn;
        SQLiteCommand cmd;
        SQLiteDataReader reader;

        public ResultController()
        {
            conn = mainController.getConnection();
            cmd = conn.CreateCommand();
        }

        public double[][] cloneMatrix(double[][] originalMatrix, int sizeMatrix)
        {
            double[][] result = new double[sizeMatrix][];

            for (int i = 0; i < sizeMatrix; i++)
            {
                result[i] = new double[sizeMatrix];
                for (int j = 0; j < sizeMatrix; j++)
                {
                    result[i][j] = originalMatrix[i][j];
                }
            }

            return result;
        }

        public double[][] transposeMatrix(double[][] matrix)
        {
            int row = matrix.Length;
            int col = matrix[0].Length;

            List<List<double>> result = new List<List<double>>();
            for (int i = 0; i < col; i++)
            {
                List<double> temp = new List<double>();
                for (int j = 0; j < row; j++)
                {
                    temp.Add(matrix[j][i]);
                }
                result.Add(temp);
            }

            return result.Select(x => x.ToArray()).ToArray();
        }
        
        public double[] pairwiseComparisonPerCriteria(string topicId, string criteriaId)
        {
            Criteria criteria = criteriaController.getCriteriaList(topicId).Single(x => x.criteriaId == Convert.ToInt32(criteriaId));

            // Get list of detail alternative for mapping
            List<DetailAlternative> detailAlternativeList = alternativeListController.getDetailListPerCriteria(topicId, criteriaId);
            int countAlternative = detailAlternativeList.Count;

            // Mapping alternativeName to index
            Dictionary<string, int> alternativeName2Idx = new Dictionary<string, int>();
            for (int i = 0; i < countAlternative; i++)
            {
                alternativeName2Idx.Add(detailAlternativeList.ElementAt(i).alternativeName, i);
            }

            // Change value = 0 to 0.0000001
            foreach (DetailAlternative detailAlternative in detailAlternativeList)
            {
                if (detailAlternative.value == 0)
                {
                    detailAlternative.value = 0.00000000000000000000000000000001;
                }
            }

            // Create 2 list of data for each pair            
            // pcData: [[alt1, alt2], [alt1, alt2], ...]
            List<List<DetailAlternative>> pcData = new List<List<DetailAlternative>>();
            for (int i = 0; i < countAlternative - 1; i++)
            {
                for (int j = i + 1; j < countAlternative; j++)
                {
                    List<DetailAlternative> oneDetail = new List<DetailAlternative>();
                    oneDetail.Add(detailAlternativeList.ElementAt(i));
                    oneDetail.Add(detailAlternativeList.ElementAt(j));
                    pcData.Add(oneDetail);
                }
            }

            // Prepare blank matrix with value 1 in main diagonal
            double[][] pcMatrix = new double[countAlternative][];
            for (int i = 0; i < countAlternative; i++)
            {
                pcMatrix[i] = new double[countAlternative];
                for (int j = 0; j < countAlternative; j++)
                {
                    if (i == j)
                    {
                        pcMatrix[i][j] = 1.0;
                    }
                }
            }
            
            // Fill other value in matrix
            foreach (List<DetailAlternative> pc in pcData)
            {
                string alternative1Name = pc.ElementAt(0).alternativeName;
                string alternative2Name = pc.ElementAt(1).alternativeName;
                double value = Convert.ToDouble(pc.ElementAt(0).value) / Convert.ToDouble(pc.ElementAt(1).value);

                int alternative1Idx, alternative2Idx;
                alternativeName2Idx.TryGetValue(alternative1Name, out alternative1Idx);
                alternativeName2Idx.TryGetValue(alternative2Name, out alternative2Idx);

                if (criteria.isFewerBetter)
                {
                    pcMatrix[alternative1Idx][alternative2Idx] = 1.0 / value;
                    pcMatrix[alternative2Idx][alternative1Idx] = value;
                }
                else
                {
                    pcMatrix[alternative1Idx][alternative2Idx] = value;
                    pcMatrix[alternative2Idx][alternative1Idx] = 1.0 / value;
                }
            }

            // Sum by column
            double[] colSum = new double[countAlternative];
            for (int i = 0; i < countAlternative; i++)
            {
                double tempSum = 0;
                for (int j = 0; j < countAlternative; j++)
                {
                    tempSum += pcMatrix[j][i];
                }
                colSum[i] = tempSum;
            }

            // Normalized Matrix
            for (int i = 0; i < countAlternative; i++)
            {
                for (int j = 0; j < countAlternative; j++)
                {
                    pcMatrix[i][j] = pcMatrix[i][j] / colSum[j];
                }
            }

            // Calculate Priority Vector
            double[] priorityVec = new double[countAlternative];
            for (int i = 0; i < countAlternative; i++)
            {
                double tempSum = 0;
                for (int j = 0; j < countAlternative; j++)
                {
                    tempSum += pcMatrix[i][j];
                }
                priorityVec[i] = tempSum / countAlternative;
            }

            return priorityVec;
        }

        public double[] criteriaPriorityVector(string topicId)
        {
            // 1. Pairwise Comparison Matrix

            // 1.1. Get list of criteria Id for mapping
            List<int> criteriaIdList = new List<int>();

            foreach (Criteria criteria in criteriaController.getCriteriaList(topicId))
            {
                criteriaIdList.Add(criteria.criteriaId);
            }

            int countCriteria = criteriaIdList.Count;

            // 1.2. Mapping criteriaId to index
            Dictionary<int, int> criteriaId2Idx = new Dictionary<int, int>();
            for (int i = 0; i < countCriteria; i++)
            {
                criteriaId2Idx.Add(criteriaIdList.ElementAt(i), i);
            }

            // 1.3. Create list of data for each criteria weight            
            // [[criteria1id, criteria2id, importancelvl], [criteria1id, criteria2id, importancelvl], ...]
            List<List<double>> cwData = new List<List<double>>();
            foreach (CriteriaWeight criteriaWeight in criteriaWeightController.getCriteriaWeightListName(topicId))
            {
                int criteria1Id = criteriaWeight.criteria1Id;
                int criteria2Id = criteriaWeight.criteria2Id;
                double importanceLevel = criteriaWeight.importanceLevel;

                int criteria1Idx, criteria2Idx;
                criteriaId2Idx.TryGetValue(criteria1Id, out criteria1Idx);
                criteriaId2Idx.TryGetValue(criteria2Id, out criteria2Idx);
                cwData.Add(new List<double>() { criteria1Idx, criteria2Idx, importanceLevel });
            }

            // 1.4. Prepare blank matrix with value 1 in main diagonal
            double[][] pcMatrix = new double[countCriteria][];
            for (int i = 0; i < countCriteria; i++)
            {
                pcMatrix[i] = new double[countCriteria];
                for (int j = 0; j < countCriteria; j++)
                {
                    if (i == j)
                    {
                        pcMatrix[i][j] = 1;
                    }
                }
            }

            // 1.5. Fill other value in matrix
            foreach (List<double> cw in cwData)
            {
                int criteria1Idx = Convert.ToInt32(cw.ElementAt(0));
                int criteria2Idx = Convert.ToInt32(cw.ElementAt(1));
                double importanceLevel = cw.ElementAt(2);

                pcMatrix[criteria1Idx][criteria2Idx] = importanceLevel;
                pcMatrix[criteria2Idx][criteria1Idx] = 1 / importanceLevel;
            }

            // 2. Normalize Matrix
            double[][] normalizedPcMatrix = cloneMatrix(pcMatrix, countCriteria);

            // 2.1. Sum by Column
            double[] colSum = new double[countCriteria];
            for (int i = 0; i < countCriteria; i++)
            {
                double tempSum = 0;
                for (int j = 0; j < countCriteria; j++)
                {
                    tempSum += pcMatrix[j][i];
                }
                colSum[i] = tempSum;
            }

            // 2.2. Divide each cell by sum of the column
            for (int i = 0; i < countCriteria; i++)
            {
                for (int j = 0; j < countCriteria; j++)
                {
                    normalizedPcMatrix[i][j] = normalizedPcMatrix[i][j] / colSum[j];
                }
            }

            // 3. Calculate Priority Vector
            double[] priorityVec = new double[countCriteria];
            for (int i = 0; i < countCriteria; i++)
            {
                double tempSum = 0;
                for (int j = 0; j < countCriteria; j++)
                {
                    tempSum += normalizedPcMatrix[i][j];
                }
                priorityVec[i] = tempSum / countCriteria;
            }

            return priorityVec;
        }

        public double[][] concatenateAllPriorityVector(string topicId)
        {
            List<string> criteriaNameList = new List<string>();
            List<string> alternativeNameList = alternativeListController.getAlternativeList(topicId);
            List<List<double>> combinedPriorityVec = new List<List<double>>();

            foreach (Criteria criteria in criteriaController.getCriteriaList(topicId))
            {
                criteriaNameList.Add(criteria.criteriaName);
                List<double> oneRow = new List<double>();
                foreach (double val in pairwiseComparisonPerCriteria(topicId, criteria.criteriaId.ToString()))
                {
                    oneRow.Add(val);
                }
                combinedPriorityVec.Add(oneRow);
            }

            double[][] combinedMat = combinedPriorityVec.Select(x => x.ToArray()).ToArray();
            double[][] transposedCombinedMat = transposeMatrix(combinedMat);

            return transposedCombinedMat;
        }

        public Dictionary<string, double> finalResult(string topicId)
        {
            List<string> alternativeNameList = alternativeListController.getAlternativeList(topicId);

            double[][] combinedMat = concatenateAllPriorityVector(topicId);
            double[] criteriaPriorityVec = criteriaPriorityVector(topicId);

            double[] finalVec = new double[alternativeNameList.Count];
            for (int i = 0; i < alternativeNameList.Count; i++)
            {
                finalVec[i] = 0;
                for (int j = 0; j < criteriaPriorityVec.Length; j++)
                {
                    finalVec[i] += combinedMat[i][j] * criteriaPriorityVec[j];
                }
            }

            Dictionary<string, double> finalResult = new Dictionary<string, double>();
            for (int i = 0; i < finalVec.Length; i++)
            {
                finalResult.Add(alternativeNameList.ElementAt(i), finalVec[i]);
            }

            return finalResult.OrderByDescending(x => x.Value).ToDictionary(x => x.Key, x => x.Value);
        }

        public List<string> bestWorstCriteria(string topicId, List<string> conclusionBestWorst)
        {
            List<string> alternativeNameList = alternativeListController.getAlternativeList(topicId);
            List<Criteria> criteriaList = criteriaController.getCriteriaList(topicId);

            double[][] combinedMat = concatenateAllPriorityVector(topicId);
            double[] criteriaPriorityVec = criteriaPriorityVector(topicId);

            double[][] finalMat = new double[alternativeNameList.Count][];
            for (int i = 0; i < alternativeNameList.Count; i++)
            {
                finalMat[i] = new double[criteriaPriorityVec.Length];
                for (int j = 0; j < criteriaPriorityVec.Length; j++)
                {
                    finalMat[i][j] += combinedMat[i][j] * criteriaPriorityVec[j];
                }
            }

            int idxAlternativeName = alternativeNameList.IndexOf(conclusionBestWorst[1]);

            List<string> bestWorstCriteria = new List<string>();
            if (conclusionBestWorst[0] == "Best")
            {
                double max = finalMat[idxAlternativeName].Max();
                for (int i = 0; i < finalMat[idxAlternativeName].Length; i++)
                {
                    if (finalMat[idxAlternativeName][i] == max)
                    {
                        bestWorstCriteria.Add(criteriaList.ElementAt(i).criteriaName);
                    }
                }
            }
            else if (conclusionBestWorst[0] == "Worst")
            {
                double min = finalMat[idxAlternativeName].Min();
                for (int i = 0; i < finalMat[idxAlternativeName].Length; i++)
                {
                    if (finalMat[idxAlternativeName][i] == min)
                    {
                        bestWorstCriteria.Add(criteriaList.ElementAt(i).criteriaName);
                    }
                }
            }

            return bestWorstCriteria;
        }

        public List<List<string>> conclusionBestWorst(string topicId)
        {
            Dictionary<string, double> result = finalResult(topicId);
            List<List<string>> conclusion = new List<List<string>>();

            if (result.Values.Max() == result.Values.Min())
            {
                conclusion = null;
            }
            else
            {
                foreach (var dict in result)
                {
                    if (dict.Value == result.Values.Max())
                    {
                        conclusion.Add(new List<string>() { "Best", dict.Key });
                    }

                    if (dict.Value == result.Values.Min())
                    {
                        conclusion.Add(new List<string>() { "Worst", dict.Key });
                    }
                }
            }

            return conclusion;
        }
    }
}
