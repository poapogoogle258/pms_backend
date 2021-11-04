package templates;

import src.Student;
import src.StudentStreamFunction;
import java.util.Comparator;
import java.util.Map;
import java.util.Optional;
import java.util.function.Predicate;
import java.util.stream.Stream;

public class StudentFunctions implements StudentStreamFunction {

  public Student findFirst(Stream<Student> studentsStream, Map<String, Predicate<?>> conditions){
    @@student_findFirst@@
  }

  public Student[] findAll(Stream<Student> studentsStream, Map<String, Predicate<?>> conditions){
    @@student_findAll@@
  }

  public boolean exists(Stream<Student> studentsStream,
                        Map<String, Predicate<?>> conditions,
                        int n){
                          @@student_exists@@
                        }

  public Student[] filterThenSort(Stream<Student> studentsStream,
                                  Map<String, Predicate<?>> conditions,
                                  Comparator<Student> comparator){
                                    @@student_filterThenSort@@
                                  }

  @@student_util@@
}
