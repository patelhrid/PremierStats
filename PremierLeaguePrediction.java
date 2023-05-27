import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.trees.J48;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.CSVLoader;

import java.io.File;

public class PremierLeaguePrediction {
    public static void main(String[] args) {
        try {
            // Step 1: Load the CSV Data
            CSVLoader loader = new CSVLoader();
            loader.setSource(new File("final_dataset.csv"));
            Instances data = loader.getDataSet();

            // Set the class index
            data.setClassIndex(data.numAttributes() - 1);

            // Step 2: Preprocess the Data (if required)
            // ...

            // Step 3: Train the Decision Tree Model (J48 algorithm)
            Classifier decisionTree = new J48();
            decisionTree.buildClassifier(data);

            // Step 4: Evaluate the Model
            Evaluation evaluation = new Evaluation(data);
            evaluation.evaluateModel(decisionTree, data);
            System.out.println(evaluation.toSummaryString());

            // Step 5: Make Predictions (optional)
            // ...

            // Step 6: Save or serialize the trained decision tree model (optional)
            // ...

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
