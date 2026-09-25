! FLAG : -floop-interchange
PROGRAM main

  IMPLICIT NONE

  INTEGER, PARAMETER :: niter = 200, ndim = 1000
  REAL    :: a(ndim,ndim), b(ndim,ndim), c(ndim,ndim)
  INTEGER :: i,j,k

  a = 1.0
  b = 2.0
  DO k = 1,niter
     DO i = 1,SIZE(a,1)
        DO j = 1,SIZE(a,2)
           c(i,j) = a(i,j) + 2*b(i,j)
        END DO
     END DO
  END DO

END PROGRAM main
