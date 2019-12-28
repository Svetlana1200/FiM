import java.util.Scanner;
public class f {
public static int the_greatest_common_divisor(int Snips, int Snails) {
int Twilight;
while (Snails > 0) {
Twilight = Snips;
Snips = Snails;
Snails = the_remainder(Twilight, Snails);
}
return Snips;
}
public static int the_remainder(int A, int B) {
int C;
int D;
int E;
C = A / B;
D = C * B;
E = A - D;
return E;
}
public static void main(String[] args) {
int Rarity;
int Applejack;
int Trixie;
System.out.println("What is first number?");
Scanner in = new Scanner(System.in);
Rarity = in.nextInt();
System.out.println("What is second number?");
Applejack = in.nextInt();
Trixie = the_greatest_common_divisor(Rarity, Applejack);
System.out.println(Trixie);
}
}