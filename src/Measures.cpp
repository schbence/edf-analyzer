#include <iostream>
#include <math.h>

using namespace std;

int my_mod(int x, int y) {
     return (x%y);
 }

 int sumitems(int *first, int nitems) {
   int i, sum = 0;
   for (i = 0; i < nitems; i++) {
     sum += first[i];
   }
   return sum;
 }

 double sumfloat(double *first, int nitems) {
   int i;
   double sum = 0.0;
   for (i = 0; i < nitems; i++) {
     sum += first[i];
   }
   return sum;
 }


double minVal (double ar[], int n)
{
   double smallest = ar[0] ;
   for ( int i=0;  i < n;  ++i ){
        if ( ar[i] < smallest ){
            smallest = ar[i] ;
         }
   }
   return smallest;
}

double maxVal (double ar[], int n)
{
    double greatest = ar[0] ;
    for ( int i=0;  i < n;  ++i ){
        if ( ar[i] > greatest ){
            greatest = ar[i] ;
         }
    }
   return greatest;
}

double log2( double number ) {
   return log( number ) / log( 2 ) ;
}

double Mean(double ar[],int n){
  double mean = 0.0;
  for (int i=0; i<n; i++){
    mean += ar[i];
  }
  mean /= n;
  return mean;
}


double STD(double ar[], int n){
  double mean = Mean(ar,n);
  double sd  = 0.0;
  for(int i=0; i<n; i++){
    double diff = mean - ar[i];
    sd += diff * diff;
  }
  sd /= n;
  return sqrt(sd);
}

double Entropy( double ar[ ] , int n, int nb ) {               // n is the length of ar[] and nb is the number of the bins
   double min = minVal(ar,n), max = maxVal(ar,n);
   if(min==max){
     return 0.0;
   }
   double lbin = (max-min)/nb;
   double bins[nb+1];
   double freq[nb+1] = {0};
   for (int i = 0; i < nb+1; ++i)
      {
         bins[i] = i*lbin;
      }
   for (int i = 0; i < n; ++i)
      {
         freq[(int) ((ar[i]-min)/lbin)]++;
      }
   double entropy=0;
   for (double fr : freq)
      {
         //cout << fr << '\n' ;
         if(fr>0){
           entropy -= fr/n * log2( fr/n ) ;
         }
      }
   //cout << "The entropy of the data: " << entropy << std::endl ;
   return entropy ;
}
