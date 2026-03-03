
# HPA Load
```
kubectl exec -it <django-pod-name> -n ecommerce -- sh
```

# for example

```
kubectl exec -it django-598459f969-qbn9q -n ecommerce -- sh
```

```
while true; do :; done
```

```
kubectl get hpa -n ecommerce -w
```
