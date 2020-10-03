 %module measures
 %include "carrays.i"
 %include "cpointer.i"
 %include "std_string.i"
 %array_class(int,intArray)
 %array_class(double, dlArray)
 %{
 /* Put header files here or function declarations like below */
 extern int my_mod(int x, int y);
 extern int sumitems(int *first, int nitems);
 extern double sumfloat(double *first, int nitems);
 extern double log2(double n);
 extern double minVal(double *arr, int nitems);
 extern double maxVal(double *arr, int nitems);
 extern double Entropy(double *first, int nitems,int nb);
 extern double Mean(double *ar, int n);
 extern double STD(double *ar, int n);

 %}
 extern int my_mod(int x, int y);
 extern int sumitems(int *first, int nitems);
 extern double sumfloat(double *first, int nitems);
 extern double log2(double n);
 extern double minVal(double *arr, int nitems);
 extern double maxVal(double *arr, int nitems);
 extern double Entropy(double *first, int nitems,int nb);
 extern double Mean(double *ar, int n);
 extern double STD(double *ar, int n);
