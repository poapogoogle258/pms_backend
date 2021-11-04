package templates;

public class FListMerge {

    public static int counter=0;

    public static void resetCounter(){
        counter=0;
    }

    /*
     * This method receives an FList and returns a new FList containing the same values but sorted in ascending order.
     *
     */
    public static FList<Integer> mergeSort(FList<Integer> fList){
        counter++;

        @@studentMergeSort@@
    }

    @@studentClass@@
}
