# install PPA-provided mosquitto 2.0.10

# disable the PPA-provided mosquitto
```
sudo service mosquitto stop
```

# Unsecured case

### run the broker
```
mosquitto -v
```

# With security sauce

### build minica
```
sudo apt install golang-go
git clone https://github.com/jsha/minica.git
cd minica
go build
```

### generate certs
```
cd certs
../minica/minica --domains localhost
```

### generate password file
```
mosquitto_passwd -c passwords user
```

### run the broker
```
mosquitto -v -c with_security.conf
```
