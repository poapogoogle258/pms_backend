package src;

import java.util.LinkedList;

public class MyStack<E> {


    private LinkedList<E> queue;

    /*
     * Constructor
     */
    public MyStack() {
        this.queue = new LinkedList<>();
    }

    /*
    * push an element at top (remember, a stack is "Last In First Out")
    */
    public void push(E elem) {
		@@student_add@@
    }

    /*
    * Return the top of the stack AND remove the retrieved element
    */
    public E pop() {
		@@student_remove@@
    }

    /*
    * Return the top element of the stack, without removing it
    */
    public E peek() {
		@@student_peek@@
    }

    /*
    * Tells if the stack is empty or not
    */
    public boolean empty() {
		@@student_isEmpty@@
    }

}
