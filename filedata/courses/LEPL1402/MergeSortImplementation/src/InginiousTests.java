package src;

import com.github.guillaumederval.javagrading.Grade;
import com.github.guillaumederval.javagrading.GradeFeedback;
import com.github.guillaumederval.javagrading.GradeFeedbacks;
import com.github.guillaumederval.javagrading.GradingRunner;
import org.junit.Test;
import org.junit.runner.RunWith;

import java.util.Random;
import java.util.Arrays;

import templates.*;

import static org.junit.Assert.*;

/*
 * Most of the code of this test suite is taken (and adapted) from an exercise of LSINF1121 course.
 * Original authors : Pierre Schaus, John Aoga
 * Modified by : Henri Piron
 */
@RunWith(GradingRunner.class)
public class InginiousTests {

    private final int arraySize = 10000;

    @Test()
    @Grade(value=1, cpuTimeout=1000)
    @GradeFeedback(onFail=true, message = "Your sort don't work properly")
    public void testSort(){
        int [] array = randomArray(arraySize);
        int [] copyArray = new int[arraySize];
        System.arraycopy(array, 0, copyArray, 0, arraySize);
        MergeSort.studentSort(array);
        Arrays.sort(copyArray);
        assertArrayEquals(copyArray, array);
    }

    /*
     * TODO: better evaluation of number of count. Sensitive to small variation in algorithm
    @Test()
    @Grade(value=1, cpuTimeout=1000)
    @GradeFeedback(onFail=true, message = "Your sort don't call the merge method enough")
    public void testNumberMergeCall(){

        MergeSort.counterRst();

        int[] array = randomArray(10000);
        MergeSort.studentSort(array);

        int count = MergeSort.getCounter();

        assertTrue(isArraySorted(array));
        assertEquals(count, 9999);

    }
    */

    @Test()
    @Grade(value=1, cpuTimeout=1000)
    @GradeFeedback(onFail=true, message = "Your merge don't work properly")
    public void testMerge(){
        int [] array = randomArray(arraySize);
        int [] copyArray = new int[arraySize];
        System.arraycopy(array, 0, copyArray, 0, arraySize);
        MergeSort.sort(array);
        Arrays.sort(copyArray);
        assertArrayEquals(copyArray, array);
    }

    @Test()
    @Grade(value=2, cpuTimeout=1000)
    @GradeFeedback(onTimeout=true, message = "Your implementation is too slow")
    @GradeFeedback(onFail=true, message = "Your method sort don't work with your method merge")
    public void testComplete(){
        int [] array = randomArray(arraySize);
        int [] copyArray = new int[arraySize];
        System.arraycopy(array, 0, copyArray, 0, arraySize);
        MergeSortBis.sort(array);
        Arrays.sort(copyArray);
        assertArrayEquals(copyArray, array);
    }

    private static int[] randomArray(int size){
        int[] array = new int[size];
        Random rng = new Random();
        for(int i = 0 ; i < size ; i++){
            array[i]= rng.nextInt(Integer.MAX_VALUE);
        }
        return array;
    }

}
