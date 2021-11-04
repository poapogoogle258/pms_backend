package src;

import com.github.guillaumederval.javagrading.Grade;
import com.github.guillaumederval.javagrading.GradeFeedback;
import com.github.guillaumederval.javagrading.GradeFeedbacks;
import com.github.guillaumederval.javagrading.GradingRunner;

import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

import templates.*;

import java.util.*;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.function.Supplier;
import java.util.stream.Collectors;
import java.util.stream.Stream;

// To have nice double numbers like 10.42
import java.math.BigDecimal;
import java.math.RoundingMode;

@RunWith(GradingRunner.class) // classic "jail runner" from Guillaume's library
public class InginiousTests {
    private StudentStreamFunction streamFunction;

    // For simplicity , use them both for first name / last name
    private String[] studentNames = new String[] {
            "Jacques", "John", "Marie", "Emma", "Olivia", "Alice", "Juliette",
            "Louise", "Jules", "Victor", "Lucas", "Gabriel", "Noah", "Hugo"
    };

    // for the section field
    private Supplier<Integer> section_rng = () -> (int) (Math.random() * 10) + 1; // between 1 and 10

    // for course grade
    private Supplier<Double> grade_rng = () -> BigDecimal
            .valueOf(Math.random() * 20)
            .setScale(2, RoundingMode.HALF_UP)
            .doubleValue();
    private String[] courses = new String[] {"Algorithmn", "Proba & Stat", "ORG"};

    // generate random students
    private Stream<Student> generate_random_students(int number) {
        List<Student> my_list = new ArrayList<>();
        for(int i = 0; i < number; i++) {
            // get random index / values
            int index = new Random().nextInt(studentNames.length);
            int index2 = new Random().nextInt(studentNames.length);
            int section = section_rng.get();
            Map<String, Double> grades = new HashMap<>();
            for(String course : courses) {
                grades.put(course, grade_rng.get());
            }
            my_list.add(new Student(studentNames[index], studentNames[index2], section, grades));
        }

        return my_list.stream();
    }

    private Map<String, Predicate<?>> generateConditions(int limit) {

        // some predicates inside
        Map<String, Predicate<?>> conditions = new HashMap<>();
        String randomName = studentNames[new Random().nextInt(studentNames.length)];
        Predicate<String> p1 = (s) -> s.equalsIgnoreCase(randomName);

        int randomInt = section_rng.get();
        Predicate<Integer> p2 = (i) -> i == randomInt;
        String courseRandom = courses[new Random().nextInt(courses.length)];
        Double d = grade_rng.get();

        Predicate<Map<String, Double>> p3 = (m) -> m.get(courseRandom) >= d;
        conditions.put("firstName", p1);
        conditions.put("lastName", p1);
        conditions.put("section", p2);
        conditions.put("courses_results", p3);

        return conditions
                .entrySet()
                .stream()
                .limit(limit)
                .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));

    }

    @Before
    public void setUp(){
        streamFunction = new StudentFunctions();
    }

    @Test
    @Grade
    @GradeFeedbacks({@GradeFeedback(message = "", onSuccess = true), @GradeFeedback(message = "findSecondAndThirdTopStudentForGivenCourse() didn't work", onFail = true, onTimeout = true)})
    public void testQuestion1() {

        for(int i = 0; i < 10; i++) {
            // random students ( at least 3 )
            Student[] random_students = generate_random_students(3 + section_rng.get()).toArray(Student[]::new);
            String course = courses[new Random().nextInt(courses.length)];

            Student[] expected = Stream
                    .of(random_students)
                    .sorted(
                            ((Comparator<Student>) (o1, o2) -> {
                                double d1 = o1.getCoursesResults().get(course);
                                double d2 = o2.getCoursesResults().get(course);
                                return Double.compare(d1, d2);
                            }).reversed()
                    )
                    .limit(3)
                    .skip(1)
                    .toArray(Student[]::new);

            Student[] result = streamFunction
                    .find_second_and_third_top_student_for_given_course(
                            Stream.of(random_students),
                            course
                    ).toArray(Student[]::new);

            assertTrue(Arrays.deepEquals(expected, result));
        }
    }

    @Test
    @Grade
    @GradeFeedbacks({@GradeFeedback(message = "", onSuccess = true), @GradeFeedback(message = "computeAverageForStudentInSection() didn't work", onFail = true, onTimeout = true)})
    public void testQuestion2() {
        for(int i = 0; i < 10; i++) {

            Student[] random_students = generate_random_students(section_rng.get()).toArray(Student[]::new);
            int section = section_rng.get();

            Object[] expected = Stream
                    .of(random_students)
                    .filter( s -> s.getSection() == section )
                    .map( student -> new Object[] {
                            String.format("%s %s %s","Student", student.getFirstName(), student.getLastName()),
                            student.getCoursesResults().values().stream().reduce(0.0, Double::sum) / (double) student.getCoursesResults().size()
                    })
                    .toArray();

            Object[] result = streamFunction.compute_average_for_student_in_section(Stream.of(random_students), section);

            assertTrue(Arrays.deepEquals(expected, result));

        }
    }

    @Test
    @Grade
    @GradeFeedbacks({@GradeFeedback(message = "", onSuccess = true), @GradeFeedback(message = "getNumberOfSuccessfulStudents() didn't work", onFail = true, onTimeout = true)})
    public void testQuestion3() {
        for(int i = 0; i < 10; i++) {

            Student[] random_students = generate_random_students(section_rng.get()).toArray(Student[]::new);

            int expected = (int) Stream
                    .of(random_students)
                    .filter( student ->
                            student.getCoursesResults()
                                    .values()
                                    .stream()
                                    .allMatch(result -> result > 10.0)
                    ).count();

            int result = streamFunction.get_number_of_successful_students(Stream.of(random_students));
            assertEquals(expected, result);
        }
    }

    @Test
    @Grade
    @GradeFeedbacks({@GradeFeedback(message = "", onSuccess = true), @GradeFeedback(message = "findLastInLexicographicOrder() didn't work", onFail = true, onTimeout = true)})
    public void testQuestion4() {
        for(int i = 0; i < 1000; i++) {

            Student[] random_students = generate_random_students(section_rng.get()).toArray(Student[]::new);

            Student expected = Stream
                    .of(random_students)
                    .sorted(
                            (o1, o2) ->
                                    Comparator
                                            .comparing(Student::getLastName, Comparator.reverseOrder())
                                            .thenComparing(Student::getFirstName, Comparator.reverseOrder())
                                            .compare(o1, o2)
                    )
                    .limit(1)
                    .findFirst()
                    .get();

            Student result = streamFunction.find_last_in_lexicographic_order(Stream.of(random_students));
            assertEquals(expected, result);
        }
    }

    @Test
    @Grade
    @GradeFeedbacks({@GradeFeedback(message = "", onSuccess = true), @GradeFeedback(message = "getFullSum() didn't work", onFail = true, onTimeout = true)})
    public void testQuestion5() {
        for(int i = 0; i < 10; i++) {

            Student[] random_students = generate_random_students(section_rng.get()).toArray(Student[]::new);

            double expected = Stream
                    .of(random_students)
                    .map(
                            student -> student
                                    .getCoursesResults()
                                    .values()
                                    .stream()
                                    .reduce(0.0, Double::sum)
                    )
                    .reduce(0.0, Double::sum);

            double result = streamFunction.get_full_sum(Stream.of(random_students));
            assertTrue(Double.compare(expected, result) == 0);
        }
    }

}