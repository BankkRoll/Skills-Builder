# 프로덕션 우수 사례: 성능 및 신뢰성 and more

# 프로덕션 우수 사례: 성능 및 신뢰성

> Express 애플리케이션의 프로덕션 환경에서 성능과 안정성을 최적화하기 위한 모범 사례를 알아봅니다. 여기에는 코드 최적화와 최적의 성능을 위한 환경 설정이 포함됩니다.

# 프로덕션 우수 사례: 성능 및 신뢰성

이 문서에서는 프로덕션 환경에 배치된 Express 애플리케이션을 위한 성능 및 신뢰성 관련 우수 사례에 대해 논의합니다.

이 주제는 명백하게 “DevOps” 분야로 구분할 수 있으며 종래의 개발 및 운영 모두를 다룹니다. 따라서, 정보는 다음과 같은 두 개의 파트로 나뉘어 있습니다.

- [코드에서 수행할 항목](#code) (개발 파트):
  - [gzip 압축 사용](#use-gzip-compression)
  - [동기식 함수 사용하지 않기](#dont-use-synchronous-functions)
  - [정확한 로깅](#do-logging-correctly)
  - [올바른 예외 처리](#exceptions)
- [환경/설정에서 수행할 항목](#env) (운영 파트):
  - [NODE_ENV를 “production”으로 설정](#set-node_env-to-production)
  - [앱이 자동으로 다시 시작되도록 보장](#ensure-your-app-automatically-restarts)
  - [앱을 클러스터에서 실행](#run-your-app-in-a-cluster)
  - [요청 결과를 캐싱](#cache-request-results)
  - [로드 밸런서 사용](#use-a-load-balancer)
  - [역방향 프록시 사용](#proxy)

## 코드에서 해야 할 일

애플리케이션의 성능을 향상시키기 위해서 코드를 통해 할 수 있는 몇 가지는 다음과 같습니다.

- [gzip 압축 사용](#use-gzip-compression)
- [동기식 함수 사용하지 않기](#dont-use-synchronous-functions)
- [정확한 로깅](#do-logging-correctly)
- [올바른 예외 처리](#exceptions)

### gzip 압축 사용

Gzip 압축을 사용하면 응답 본문의 크기를 크게 줄일 수 있으며, 따라서 웹 앱의 속도를 높일 수 있습니다. Express 앱에서 gzip 압축을 사용하려면 [compression](https://www.npmjs.com/package/compression) 미들웨어를 사용하십시오. 예를 들면 다음과 같습니다.

```
const compression = require('compression')
const express = require('express')
const app = express()

app.use(compression())
```

많은 트래픽이 발생하는 프로덕션 환경의 웹사이트의 경우, 압축을 실행하는 가장 좋은 방법은 역방향 프록시 레벨에서 압축을 구현하는 것입니다([역방향 프록시 사용](#proxy) 참조). 그러한 경우에는 compression 미들웨어를 사용할 필요가 없습니다. Nginx에서 gzip 압축을 사용하는 방법에 대한 자세한 내용은 Nginx 문서의 [Module ngx_http_gzip_module](http://nginx.org/en/docs/http/ngx_http_gzip_module.html)을 참조하십시오.

### 동기식 함수 사용하지 않기

동기식 함수 및 메소드는 리턴될 때까지 실행 프로세스를 묶어 둡니다. 동기식 함수에 대한 한 건의 호출은 몇 마이크로초 또는 밀리초 내에 리턴될 수도 있지만, 많은 트래픽이 발생하는 웹사이트에서 이러한 동기식 호출들이 합산되면 앱의 성능이 낮아집니다. 프로덕션 환경에서는 동기식 함수의 사용을 피하십시오.

Node 및 다수의 모듈은 동기식 및 비동기식 버전의 함수를 제공하지만, 프로덕션 환경에서는 항상 비동기식 버전을 사용하십시오. 동기식 함수의 사용이 정당화되는 유일한 경우는 초기 시작 시에 사용되는 경우입니다.

애플리케이션이 동기 API를 사용할 때마다 경고 메시지와 스택 트레이스를 출력하려면 –trace-sync-io 명령줄 플래그를 사용할 수 있습니다. 물론, 프로덕션 환경에서 이러한 플래그를 실제로 사용해서는 안 되며, 이는 코드가 프로덕션 환경에서 사용될 준비가 되었다는 것을 보장하기 위한 것입니다. 자세한 정보는 [node 커맨드라인 옵션 문서](https://nodejs.org/api/cli.html#cli_trace_sync_io)를 참조하십시오.

### 올바른 로깅 방법을 사용해야 합니다

일반적으로 앱은 디버깅 그리고 앱 활동 로깅(사실상 디버깅 이외의 모든 것)이라는 두 가지 이유로 인해 로깅을 실행합니다. `console.log()` 또는 `console.err()`을 사용하여 터미널에 로그 메시지를 출력하는 것이 일반적인 개발 작업 방식입니다. 단, [이 함수들은](https://nodejs.org/api/console.html#console) 출력 대상이 터미널이나 파일일 경우 동기적으로 동작하므로, 출력 결과를 다른 프로그램으로 파이프하지 않는 이상 프로덕션 환경에서는 적합하지 않습니다.

#### 디버깅의 경우

디버깅을 위해 로깅하는 경우에는 `console.log()`를 사용하는 대신 [debug](https://www.npmjs.com/package/debug)와 같은 특별한 디버깅 모듈을 사용하십시오. 이러한 모듈을 이용하면 DEBUG 환경 변수를 사용하여 디버그 메시지 발생 시 어떠한 디버그 메시지가 `console.err()`로 전송되는지 제어할 수 있습니다. 앱을 순수한 비동기식으로 유지하려면 `console.err()`을 다른 프로그램으로 전송해야 합니다. 그러나 아마도 프로덕션 단계에서 디버그를 수행할 필요는 없을 것입니다.

#### 앱 활동의 경우

애플리케이션 활동(예: 트래픽 추적 또는 API 호출 기록)을 로깅할 때는 console.log() 대신 [Pino](https://www.npmjs.com/package/pino)와 같은 로깅 라이브러리를 사용하는 것이 좋습니다. Pino는 가장 빠르고 효율적인 옵션입니다.

### 올바른 예외 처리

Node 앱은 처리되지 않은 예외가 발생할 때 충돌이 발생합니다. 예외를 처리하지 않고 적절한 조치를 취하지 않으면 Express 앱에서 충돌이 발생하고 오프라인 상태가 됩니다. 아래의 [앱이 자동으로 다시 시작되도록 보장](#restart)의 조언을 따르면 앱은 충돌에서부터 복원될 것입니다. 다행히 Express 앱의 일반적인 시작 시간은 짧습니다. 그럼에도 불구하고, 먼저 앱의 충돌을 피하는 것이 중요하며, 이를 위해서는 예외를 올바르게 처리해야 합니다.

모든 예외를 처리하도록 보장하려면 다음의 기법을 사용하십시오.

- [try-catch 사용](#try-catch)
- [프로미스 사용](#promises)

이 주제에 대해 자세히 살펴보기 전에 먼저 Node/Express의 오류 처리, 즉 오류 우선(error-first) 콜백의 사용 및 미들웨어를 통한 오류의 전파에 대한 기본적인 사항을 이해해야 합니다. Node는 비동기식 함수로부터 오류를 리턴하기 위해 “오류 우선 콜백” 방식을 사용하며, 여기서 콜백 함수의 첫 번째 매개변수는 오류 오브젝트이고 그 후속 매개변수에 결과 데이터가 뒤따릅니다. 오류가 없음을 나타낼 때는 첫 번째 매개변수로 널(null)을 전달합니다. 의미 있는 방식으로 오류를 처리하려면 콜백 함수는 이에 맞게 오류 우선 콜백 방식을 따라야 합니다. 그리고 Express에서의 우수 사례는 next() 함수를 사용하여 미들웨어 체인을 통해 오류를 전파하는 것입니다.

오류 처리의 기본사항 대한 자세한 내용은 다음을 참조하십시오.

- [Node.js의 오류 처리](https://www.tritondatacenter.com/node-js/production/design/errors)

#### try-catch 사용

Try-catch는 동기식 코드에서 예외를 처리하는 데 사용할 수 있는 JavaScript 언어 구조체입니다. 예를 들면, try-catch를 사용하여 아래와 같이 JSON 구문 분석 오류를 처리할 수 있습니다.

아래에는 try-catch를 사용하여 잠재적인 프로세스 충돌 예외를 처리하는 예가 표시되어 있습니다.
이 미들웨어 함수는 JSON 오브젝트이자 “params”라는 이름을 갖는 조회 필드를 수락합니다.

```
app.get('/search', (req, res) => {
  // Simulating async operation
  setImmediate(() => {
    const jsonStr = req.query.params
    try {
      const jsonObj = JSON.parse(jsonStr)
      res.send('Success')
    } catch (e) {
      res.status(400).send('Invalid JSON string')
    }
  })
})
```

그러나 try-catch는 동기식 코드에 대해서만 작동합니다. Node 플랫폼은 기본적으로 비동기식이므로(특히, 프로덕션 환경의 경우), try-catch를 통해 많은 예외를 처리할 수는 없을 것입니다.

#### 프로미스 사용

async 함수 내에서 에러가 발생하거나, async 함수 안에서 거부된(rejected) 프로미스를 await 할 경우, 해당 에러는`next(err)`를 호출한 것과 동일하게 에러 핸들러로 전달됩니다.
자세한 내용은 Node.js 에러 처리 문서를 참고하시기 바랍니다.

```
app.get('/', async (req, res, next) => {
  const data = await userData() // If this promise fails, it will automatically call `next(err)` to handle the error.

  res.send(data)
})

app.use((err, req, res, next) => {
  res.status(err.status ?? 500).send({ error: err.message })
})
```

또한 미들웨어에 비동기 함수를 사용할 수 있으며, 만약 프로미스가 실패할 경우 라우터가 자동으로 에러를 처리합니다 예를 들면 다음과 같습니다.

```
app.use(async (req, res, next) => {
  req.locals.user = await getUser(req)

  next() // This will be called if the promise does not throw an error.
})
```

성능과 유지 보수 측면에서 가장 좋은 방법은 에러를 가능한 발생 지점 가까이에서 처리하는 것입니다. 따라서 라우터가 에러를 처리할 수 있더라도 별도의 에러 처리 미들웨어에 의존하기보다 미들웨어 내에서 에러를 직접 잡아 처리하는 것이 권장됩니다.

#### 하지 말아야 할 일

수행하지 *않아야* 할 한 가지 항목은 예외가 이벤트 루프에까지 발생할 때 생성되는 `uncaughtException` 이벤트를 청취하는 것입니다. `uncaughtException`에 대한 이벤트 리스너를 추가하면 예외가 발생하는 프로세스의 기본 작동을 변경할 수 있으며, 해당 프로세스는 예외가 발생하더라도 계속하여 실행될 것입니다. 이러한 방법은 앱에서 충돌이 발생하는 것을 방지하는 좋은 방법인 것처럼 보일 수 있지만, 처리되지 않은 예외가 발생한 후에도 앱이 계속하여 실행되면 프로세스가 불안정하고 예측할 수 없는 상태가 되므로 이러한 방법은 위험한 작업 방식이며 권장되지 않습니다.

또한 `uncaughtException`을 사용하는 것은 [세련되지 못한 방식](https://nodejs.org/api/process.html#process_event_uncaughtexception)인 것으로 공식적으로 인식되고 있으며, 코어로부터 이러한 방식을 제거하는 방법이 [제안](https://github.com/nodejs/node-v0.x-archive/issues/2582)되어 있습니다. 따라서 `uncaughtException`을 청취하는 것은 좋은 생각이 아닙니다. 따라서 여러 프로세스 및 수퍼바이저의 사용 등을 권장하며, 오류로부터 복구되는 가장 안정적인 방법은 충돌이 발생한 후 다시 시작하는 것인 경우가 많습니다.

[도메인](https://nodejs.org/api/domain.html)의 사용 또한 권장하지 않습니다. 일반적으로 도메인은 문제를 해결하지 못하며, 더 이상 사용되지 않는 모듈입니다.

## 환경/설정에서 수행할 항목

앱의 성능을 향상시키기 위해서 시스템 환경에서 할 수 있는 몇 가지는 다음과 같습니다.

- [NODE_ENV를 “production”으로 설정](#set-node_env-to-production)
- [앱이 자동으로 다시 시작되도록 보장](#ensure-your-app-automatically-restarts)
- [앱을 클러스터에서 실행](#run-your-app-in-a-cluster)
- [요청 결과를 캐싱](#cache-request-results)
- [로드 밸런서 사용](#use-a-load-balancer)
- [역방향 프록시 사용](#proxy)

### NODE_ENV를 “production”으로 설정

NODE_ENV 환경 변수는 애플리케이션이 실행되는 환경(일반적으로 개발 환경 또는 프로덕션 환경)을 지정합니다. 성능을 향상하는 가장 간단한 방법 중 하나는 환경 변수 NODE_ENV를 `production`으로 설정하는 것입니다.

NODE_ENV를 “production”으로 설정하면 Express는 다음과 같이 동작합니다.

- 보기 템플리트를 캐싱.
- CSS 확장기능을 통해 생성된 CSS 파일을 캐싱.
- 더 간결한 오류 메시지를 생성.

[테스트 결과에 따르면]((https://www.dynatrace.com/news/blog/the-drastic-effects-of-omitting-node-env-in-your-express-js-applications/) NODE_ENV를 production으로 설정하는 것만으로도 애플리케이션 성능이 3배 향상될 수 있음이 확인되었습니다.

특정한 환경을 위한 코드를 작성하는 경우, `process.env.NODE_ENV`를 통해 NODE_ENV의 값을 확인할 수 있습니다. 환경 변수의 값을 확인하는 작업은 성능 저하를 유발하므로 이러한 작업은 낮은 빈도로 실행해야 한다는 점에 주의하십시오.

일반적으로 개발 시에는, 예를 들면 `export` 또는 `.bash_profile` 파일을 이용하여 대화식 쉘에서 환경 변수를 설정할 수 있습니다. 하지만 일반적으로 프로덕션 서버에서는 직접 설정하지 않고, 대신 운영체제의 초기화 시스템(systemd 등) 사용하는 것이 권장됩니다. 다음 섹션에서 일반적인 init 시스템의 사용에 대한 자세한 내용을 확인할 수 있지만, NODE_ENV를 설정하는 것은 성능에 매우 중요하므로(또한 쉽게 실행할 수 있으므로) NODE_ENV의 설정을 여기서 강조합니다.

systemd를 이용하는 경우, 유닛 파일에 `Environment` 지시문을 사용하십시오. 예를 들면 다음과 같습니다.

```
# /etc/systemd/system/myservice.service
Environment=NODE_ENV=production
```

자세한 내용은 [systemd 유닛에서 환경 변수 사용하기를](https://www.flatcar.org/docs/latest/setup/systemd/environment-variables/) 참고하시기 바랍니다.

### 앱이 자동으로 다시 시작되도록 보장

프로덕션 환경에서 애플리케이션이 오프라인 상태가 되어서는 절대로 안 됩니다. 따라서 앱에서 충돌이 발생하거나 서버 자체에서 충돌이 발생하는 경우 모두 앱이 다시 시작되도록 해야 합니다. 이러한 일 중 어느 하나라도 발생하지 않는 것이 바람직하지만, 현실적으로는 다음과 같은 방법을 통해 이 두 가지 만일의 사태를 처리해야 합니다.

- 앱에서 충돌이 발생하는 경우 프로세스 관리자를 사용하여 앱(및 Node)을 다시 시작.
- OS에서 충돌이 발생하는 경우 해당 OS에서 제공하는 init 시스템을 사용하여 프로세스 관리자를 다시 시작. 프로세스 관리자 없이도 init 시스템을 사용할 수 있습니다.

처리되지 않은 예외가 발생하는 경우 Node 애플리케이션에서 충돌이 발생합니다. 가장 먼저 해야 할 일은 앱의 테스트가 잘 이루어지도록 하고 앱이 모든 예외를 처리하도록 하는 것입니다(자세한 내용은 [올바른 예외 처리](#exceptions)를 참조). 그러나 하나의 안전 장치로서, 앱에서 충돌이 발생하는 경우에 앱이 자동으로 다시 시작되도록 하는 메커니즘을 실행하십시오.

#### 프로세스 관리자 사용

개발 시에는 단순히 명령행에서 `node server.js` 또는 이와 유사한 명령을 실행하여 앱을 시작했습니다. 그러나 프로덕션 환경에서 이러한 방식으로 앱을 실행하는 것은 매우 위험합니다. 앱에서 충돌이 발생하면 앱은 다시 시작될 때까지 오프라인 상태가 됩니다. 앱에서 충돌이 발생할 때 앱이 다시 시작되도록 하려면 프로세스 관리자를 사용하십시오. 프로세스 관리자는 애플리케이션을 위한 “컨테이너”이며, 배치 작업을 용이하게 하고, 높은 가용성을 제공하고, 런타임 시에 애플리케이션을 관리할 수 있도록 합니다.

앱에서 충돌이 발생할 때 앱이 다시 시작되도록 하는 것 이외에도, 프로세스 관리자를 통해 다음을 실행할 수 있습니다.

- 런타임 성능 및 자원 소비에 대한 통찰력을 획득.
- 성능 향상을 위해 설정을 동적으로 수정.
- 제어 클라스터링 (pm2)

과거에는 [PM2](https://github.com/Unitech/pm2)와 같은 Node.js 프로세스 매니저를 사용하는 것이 널리 퍼져 있었습니다. 원하신다면 해당 문서를 참고하시기 바랍니다. 하지만 프로세스 관리를 위해서는 init 시스템을 사용하는 것을 권장합니다.

#### init 시스템 사용

신뢰성의 다음 단계는 서버가 다시 시작될 때 애플리케이션이 다시 시작되도록 하는 것입니다. 시스템은 여전히 여러 이유로 작동이 중단될 수 있습니다. 서버에서 충돌이 발생할 때 앱이 다시 시작되도록 하려면 OS에 내장된 init 시스템을 사용하십시오. 현재 가장 널리 사용되는 init 시스템은 [systemd](https://wiki.debian.org/systemd)입니다.

Express 앱에 init 시스템을 사용하는 데에는 다음과 같은 두 가지 방법이 있습니다.

- 프로세스 관리자에서 앱을 실행한 후, init 시스템을 통해 프로세스 관리자를 서비스로서 설치하십시오. 프로세스 관리자는 앱에서 충돌이 발생할 때 앱을 자동으로 시작하고, init 시스템은 OS가 다시 시작될 때 프로세스 관리자를 다시 시작할 것입니다. 이러한 접근법은 권장되는 접근법입니다.
- init 시스템을 통해 직접 앱(및 Node)을 실행하십시오. 이 방법은 조금 더 간편하지만, 프로세스 관리자의 사용을 통한 추가적인 이점을 얻을 수 없습니다.

##### Systemd

Systemd는 Linux용 시스템 및 서비스 관리자입니다. 대부분의 주요 Linux 배포판은 systemd를 기본 init 시스템으로 도입했습니다.

systemd 서비스 구성 파일은 *유닛 파일(unit file)*로 불리며, 파일 이름이 .service로 끝납니다. 아래는 Node 애플리케이션을 직접 관리하기 위한 파일 예시입니다. 시스템과 애플리케이션에 맞게 `<angle brackets>` 로 표시된 값을 교체하시기 바랍니다.

```
[Unit]
Description=<Awesome Express App>

[Service]
Type=simple
ExecStart=/usr/local/bin/node </projects/myapp/index.js>
WorkingDirectory=</projects/myapp>

User=nobody
Group=nogroup

# Environment variables:
Environment=NODE_ENV=production

# Allow many incoming connections
LimitNOFILE=infinity

# Allow core dumps for debugging
LimitCORE=infinity

StandardInput=null
StandardOutput=syslog
StandardError=syslog
Restart=always

[Install]
WantedBy=multi-user.target
```

systemd에 대한 자세한 정보는 [systemd 참조 자료(man page)](http://www.freedesktop.org/software/systemd/man/systemd.unit.html)를 참조하십시오.

### 앱을 클러스터에서 실행

멀티코어 시스템에서는 프로세스 클러스터를 실행하여 Node 앱의 성능을 여러 배 높일 수 있습니다. 클러스터는 해당 앱의 인스턴스를 여러 개 실행하여(이상적인 경우 각 CPU 코어에서 하나의 인스턴스를 실행) 인스턴스들 사이에서 로드 및 태스크를 분배합니다.

![클러스터 API를 사용한 애플리케이션 인스턴스간 부하 분산](https://expressjs.com/images/clustering.png)

중요: 앱 인스턴스들은 별도의 프로세스로서 실행되므로 이러한 인스턴스들은 동일한 메모리 공간을 공유하지 않습니다. 즉, 오브젝트는 해당 앱의 각 인스턴스에 대한 로컬 오브젝트입니다. 따라서 애플리케이션 코드 내의 상태를 유지보수할 수 없습니다. 그러나 [Redis](http://redis.io/)와 같은 인메모리 데이터 저장소를 사용하면 세션과 관련된 데이터 및 상태를 저장할 수 있습니다. 이러한 주의사항은 기본적으로 여러 프로세스를 이용한 클러스터링 또는 여러 대의 실제 서버를 이용한 클러스터링 등 모든 형태의 수평적 확장에 적용됩니다.

클러스터화된 앱에서 작업자 프로세스는 나머지 프로세스에 영향을 미치지 않으면서 개별적으로 충돌이 발생할 수 있습니다. 성능상의 이점 이외에도, 실패 격리는 앱 프로세스 클러스터를 실행해야 하는 또 다른 이유가 됩니다. 한 작업자 프로세스에서 충돌이 발생할 때마다, 항상 반드시 해당 이벤트를 로깅하고 cluster.fork()를 이용해 새로운 프로세스를 복제생성하십시오.

#### Node의 cluster 모듈 사용

클러스터링은 Node의 [cluster 모듈](https://nodejs.org/api/cluster.html)을 통해 가능합니다. 이러한 클러스터링을 통해 마스터 프로세스는 여러 작업자 프로세스를 복제생성하고, 수신되는 연결을 여러 작업자 사이에서 분배할 수 있습니다.

#### PM2 사용

애플리케이션을 PM2에 배치하면, 애플리케이션 코드를 수정하지 *않고도* 클러스터링을 활용할 수 있습니다. 먼저 [애플리케이션이 상태 비저장(stateless)](https://pm2.keymetrics.io/docs/usage/specifics/#stateless-apps)인지 확인해야 합니다 즉, 프로세스 내에 세션, 웹소켓 연결 등 로컬 데이터가 저장되어 있지 않아야 합니다.

PM2로 애플리케이션을 실행하고 있을 때, 특정한 수의 인스턴스에 실행하는 **클러스터 모드**를 켤 수 있습니다. 머신의 가용 CPU 수같은 것들이 특정한 수입니다. 애플리케이션을 끌 필요 없이 `pm2` 커맨드라인 명령을 이용해 클러스터에 있는 프로세스의 수를 직접 바꿀 수도 있습니다.

아래와 같은 방법으로 클러스터 모드를 킵니다.

```
# Start 4 worker processes
$ pm2 start npm --name my-app -i 4 -- start
# Auto-detect number of available CPUs and start that many worker processes
$ pm2 start npm --name my-app -i max -- start
```

이 수는 PM2 프로세스 파일 (`ecosystem.config.js`나 그와 유사한 파일) 안의 `exec_mode`를 `cluster`나 `instances`를 설정해서 수정될 수 있습니다.

실행이 시작되면, `app`으로 이름지어진 애플리케이션을 아래와 같은 방법으로 스케일링 할 수 있습니다.

```
# Add 3 more workers
$ pm2 scale my-app +3
# Scale to a specific number of workers
$ pm2 scale my-app 2
```

PM2의 클러스터링에 관한 추가 정보는 PM2 문서의 [Cluster Mode](https://pm2.keymetrics.io/docs/usage/cluster-mode/)를 참고해주세요.

### 요청 결과를 캐싱

프로덕션 환경 내에서의 성능을 향상시키기 위한 또 다른 전략은 요청의 결과를 캐싱하여 앱이 동일한 요청을 반복적으로 제공하는 작업을 반복하지 않도록 하는 것입니다.

애플리케이션의 속도와 성능을 크게 향상시키려면 [Varnish](https://www.varnish-cache.org/) 또는 [Nginx](https://blog.nginx.org/blog/nginx-caching-guide)와 같은 캐싱 서버를 사용하는 것이 좋습니다.
(참고: [Nginx 캐싱 가이드](https://serversforhackers.com/nginx-caching/))

### 로드 밸런서 사용

앱의 최적화 수준에 상관없이, 하나의 인스턴스는 제한된 양의 로드 및 트래픽만을 처리할 수 있습니다. 앱을 확장하는 방법 중 하나는 해당 앱의 인스턴스를 여러 개 실행하고 로드 밸런서를 통해 트래픽을 분배하는 것입니다. 로드 밸런서를 설정하면 앱의 성능 및 속도를 향상시킬 수 있으며, 하나의 인스턴스를 이용할 때보다 훨씬 더 높은 수준으로 확장할 수 있습니다.

로드 밸런서는 일반적으로 여러 애플리케이션 인스턴스 및 서버에 대한 트래픽을 오케스트레이션하는 역방향 프록시입니다. 애플리케이션의 로드 밸런서를 손쉽게 구축하려면 [Nginx](https://nginx.org/en/docs/http/load_balancing.html)또는 [HAProxy](https://www.digitalocean.com/community/tutorials/an-introduction-to-haproxy-and-load-balancing-concepts)를 활용할 수 있습니다.

로드 밸런싱을 이용하는 경우, 특정한 세션 ID와 연관된 요청이 해당 요청을 발생시킨 프로세스에 연결되도록 해야 할 수도 있습니다. 이러한 경우는 *세션 선호도(session affinity)* 또는 *스티키 세션(sticky session)*으로 알려져 있으며, 세션 데이터를 위해 Redis와 같은 데이터 저장소를 사용하는 위의 제안을 통해 처리할 수도 있습니다(애플리케이션에 따라 다름). 토론을 위해서는 [Using multiple nodes](https://socket.io/docs/v4/using-multiple-nodes/)를 참조하십시오.

### 역방향 프록시 사용

역방향 프록시는 웹 앱의 프론트에 위치하며, 요청이 앱으로 전달되도록 할 뿐만 아니라 요청에 대한 지원 연산을 수행합니다. 이는 오류 페이지, 압축, 캐싱, 파일 제공, 로드 밸런싱 및 기타 여러 작업을 처리할 수 있습니다.

애플리케이션 상태를 알아야 할 필요가 없는 태스크를 역방향 프록시로 이양하면 Express는 더 적은 자원을 차지하게 되어 특성화된 애플리케이션 태스크를 수행할 수 있습니다. 이러한 이유로 프로덕션환경에서는 Express를 [Nginx](https://www.nginx.org/) 또는 [HAProxy](https://www.haproxy.org/)와 같은 리버스 프록시 뒤에서 실행하는 것을 권장합니다.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/advanced/best-practice-performance.md          )

---

# 프로덕션 우수 사례: 보안

> Express 애플리케이션을 프로덕션 환경에서 운영할 때 반드시 지켜야 할 중요한 보안 모범 사례를 알아봅니다. 여기에는 TLS 사용, 입력값 검증, 보안 쿠키 설정, 그리고 다양한 취약점 예방 방법이 포함됩니다.

# 프로덕션 우수 사례: 보안

## 개요

**“프로덕션 (production)”** 이라는 용어는 소프트웨어 라이프사이클 중 애플리케이션 또는 API가 최종 사용자 또는 소비자에게 정식으로 제공되는 단계를 말합니다. 이와 반대로 *“개발(development)”* 단계에서는 아직 코드가 활발하게 작성 및 테스트되며 애플리케이션은 외부 액세스에 개방되지 않습니다. 이에 대응하는 시스템 환경은 각각 *프로덕션* 환경 및 *개발* 환경이라고 부릅니다.

개발 환경 및 프로덕션 환경은 일반적으로 서로 다르게 설정되며 두 환경의 요구사항은 크게 다릅니다. 개발 환경에서는 좋은 것일지라도 프로덕션 환경에서는 허용되지 않을 수도 있습니다. 예를 들면, 개발 환경에서는 디버깅을 위해 상세한 오류 로깅이 선호될 수 있지만, 이러한 행동은 프로덕션 환경에서 보안 우려사항이 될 수 있습니다. 그리고 개발 환경에서는 확장성, 신뢰성 및 성능에 대해 걱정할 필요가 없지만, 이러한 요인들은 프로덕션 환경에서 매우 중요해집니다.

참고

만약 Express에서 보안 취약점을 발견하셨다면, [보안 정책 및 절차](https://expressjs.com/en/resources/contributing.html#security-policies-and-procedures)를 참고하시기 바랍니다.

이 문서에서는 프로덕션 환경에 배치된 Express 애플리케이션을 위한 몇 가지 보안 우수 사례에 대해 논의합니다.

- [프로덕션 모범 사례: 보안](#production-best-practices-security)
  - [개요](#overview)
  - [Express의 사용 중단되었거나 취약한 버전을 사용하지 않습니다](#dont-use-deprecated-or-vulnerable-versions-of-express)
  - [TLS 사용](#use-tls)
  - [사용자 입력을 신뢰하지 않습니다](#do-not-trust-user-input)
    - [오픈 리다이렉트를 방지합니다](#prevent-open-redirects)
  - [Helmet 사용](#use-helmet)
  - [지문 인식 감소](#reduce-fingerprinting)
  - [쿠키를 안전하게 사용](#use-cookies-securely)
    -
    - [ieNoOpen](https://github.com/helmetjs/ienoopen)은 IE8 이상에 대해 `X-Download-Options`를 설정합니다.
  - [인증 체계에 대한 브루스 포트 공격 방지](#prevent-brute-force-attacks-against-authorization)
  - [종속 항목이 안전한지 확인](#ensure-your-dependencies-are-secure)
    - [그 외의 알려져 있는 취약점 회피](#avoid-other-known-vulnerabilities)
  - [추가적인 고려사항](#additional-considerations)

## 더 이상 사용되지 않거나 취약성이 있는 버전의 Express를 사용 중지

Express 2.x 및 3.x에 대한 유지보수는 더 이상 이루어지지 않습니다. 이러한 버전에서의 보안 및 성능 문제는 수정되지 않습니다. 이러한 버전은 사용하지 마십시오! 아직 버전 4로 이전하지 않은 경우에는 [마이그레이션 안내서](https://expressjs.com/ko/guide/migrating-4.html)를 따르십시오.

또한 [보안 업데이트 페이지](https://expressjs.com/ko/advanced/security-updates.html)의 목록에 포함된 취약성 있는 Express 버전을 사용하고 있지 않은지 확인하십시오. 취약성 있는 Express 버전을 사용하고 있는 경우에는 안정적인 릴리스 중 하나로 업데이트해야 하며, 가능하면 최신 버전으로 업데이트하는 것이 좋습니다.

## TLS 사용

앱이 민감한 데이터를 다루거나 전송하는 경우에는 [전송 계층 보안](https://en.wikipedia.org/wiki/Transport_Layer_Security)(TLS)을 사용하여 연결 및 데이터를 보호하십시오. 이 기술은 데이터를 클라이언트로부터 서버로 전송하기 전에 데이터를 암호화하며, 따라서 몇 가지 일반적인(그리고 쉬운) 해킹을 방지합니다. Ajax 및 POST 요청은 브라우저에서 분명하게 보이지 않고 “숨겨진” 것처럼 보일 수도 있지만, 이러한 요청의 트래픽은 [패킷 가로채기](https://en.wikipedia.org/wiki/Packet_analyzer) 및 [중간자 공격](https://en.wikipedia.org/wiki/Man-in-the-middle_attack)에 취약합니다.

여러분은 SSL(Secure Socket Layer) 암호화에 익숙할 것입니다. [TLS는 단순히 SSL이 다음 단계로 발전된 형태입니다](https://msdn.microsoft.com/en-us/library/windows/desktop/aa380515\(v=vs.85\).aspx). 즉, 이전에 SSL을 사용했다면 TLS로의 업그레이드를 고려해야 합니다. 일반적으로 TLS의 처리를 위해서는 Nginx를 권장합니다. Nginx(및 기타 서버)에서 TLS를 구성하는 방법에 대한 좋은 참조 자료를 확인하려면 [Recommended Server Configurations(Mozilla Wiki)](https://wiki.mozilla.org/Security/Server_Side_TLS#Recommended_Server_Configurations)를 참조하십시오.

또한 무료 TLS 인증서를 얻기 위한 편리한 도구 중 하나는 [Internet Security Research Group(ISRG)](https://letsencrypt.org/isrg/)이 제공하는 무료의 자동 개방형 인증 기관(CA)인 [Let’s Encrypt](https://letsencrypt.org/about/)입니다.

## 사용자 입력을 신뢰하지 않습니다

웹 애플리케이션에서 가장 중요한 보안 요구 사항 중 하나는 적절한 사용자 입력 검증 및 처리를 수행하는 것입니다. 이는 여러 형태로 나타나며, 이 문서에서는 모든 경우를 다루지 않습니다.
궁극적으로 애플리케이션이 수용하는 사용자 입력 유형을 검증하고 올바르게 처리하는 책임은 개발자에게 있습니다.

### 오픈 리다이렉트 방지

잠재적으로 위험한 사용자 입력의 예로 오픈 리다이렉트가 있습니다. 이는 애플리케이션이 URL을 사용자 입력으로 받아들여 (예: `?url=https://example.com` 쿼리 문자열)
 `res.redirect`를 사용해 `location` 헤더를 설정하고 3xx 상태 코드를 반환하는 경우입니다.

애플리케이션은 악성 링크(예: 피싱 사이트) 로 사용자를 유도하는 위험을 방지하기 위해, 들어오는 URL에 대해 리다이렉트를 허용하는지 반드시 검증해야 합니다.

아래는 `res.redirect` 또는 `res.location`을 사용하기 전에 URL을 검증하는 예시입니다.

```
app.use((req, res) => {
  try {
    if (new Url(req.query.url).host !== 'example.com') {
      return res.status(400).end(`Unsupported redirect to host: ${req.query.url}`)
    }
  } catch (e) {
    return res.status(400).end(`Invalid url: ${req.query.url}`)
  }
  res.redirect(req.query.url)
})
```

## Helmet 사용

[Helmet](https://www.npmjs.com/package/helmet)을 이용하면 HTTP 헤더를 적절히 설정하여 몇 가지 잘 알려진 웹 취약성으로부터 앱을 보호할 수 있습니다.

Helmet은 보안 관련 HTTP 응답 헤더를 설정하는 미들웨어 함수입니다. Helmet은 기본적으로 다음 헤더들을 설정합니다.

- `Content-Security-Policy`: 페이지에서 허용되는 콘텐츠를 강력하게 지정하여 여러 공격을 완화합니다.
- `Cross-Origin-Opener-Policy`: 페이지의 프로세스 격리를 돕습니다.
- `Cross-Origin-Resource-Policy`: 다른 출처가 리소스를 크로스 오리진으로 로드하는 것을 차단합니다.
- `Origin-Agent-Cluster`: 프로세스 격리를 출처(origin) 단위로 변경합니다.
- `Referrer-Policy`: [Referer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer) 헤더를 제어합니다.
- `Strict-Transport-Security`: 브라우저에 HTTPS를 우선 사용하도록 지시합니다.
- `X-Content-Type-Options`: [MIME 스니핑](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types#mime_sniffing)을 방지합니다.
- `X-DNS-Prefetch-Control`: DNS 프리페칭 제어를 담당합니다.
- `X-Download-Options`: 다운로드를 저장하도록 강제합니다 (인터넷 익스플로러 전용)
- `X-Frame-Options`: [클릭재킹](https://en.wikipedia.org/wiki/Clickjacking) 공격을 완화하기 위한 레거시 헤더입니다.
- `X-Permitted-Cross-Domain-Policies`: Acrobat과 같은 Adobe 제품의 크로스 도메인 동작을 제어합니다.
- `X-Powered-By`: 웹 서버 정보에 관한 헤더입니다. 해당 헤더는 단순 공격에 악용될 수 있어 제거되었습니다
- `X-XSS-Protection`: [XSS 공격](https://developer.mozilla.org/en-US/docs/Glossary/Cross-site_scripting)을 완화하려 했던 레거시 헤더이나, 오히려 문제를 악화시키기 때문에 Helmet에서는 비활성화합니다

각 헤더는 필요에 따라 설정하거나 비활성화할 수 있습니다. 자세한 내용은 [Helmet 공식 문서를](https://helmetjs.github.io/) 참고하시기 바랍니다.

다른 모든 모듈처럼 Helmet은 다음과 같이 설치할 수 있습니다.

```
$ npm install helmet
```

코드에서 Helmet을 사용하는 방법은 문서를 참고하세요

```
// ...

const helmet = require('helmet')
app.use(helmet())

// ...
```

## 지문 인식(Fingerprinting) 감소

서버가 사용하는 소프트웨어를 공격자가 식별하는 능력을 줄이는 것은 추가적인 보안 계층을 제공할 수 있습니다. 이를 ‘지문 인식(fingerprinting)’이라 합니다. 비록 지문 인식 자체가 직접적인 보안 문제는 아니지만, 이를 줄임으로써 전체적인 보안 수준이 향상됩니다.
서버 소프트웨어는 특정 요청에 대한 응답 방식, 예를 들어 HTTP 응답 헤더 등에서 특이점을 통해 식별될 수 있습니다.

따라서 우수 사례는 다음과 같이 `app.disable()` 메소드를 이용해 이 헤더를 끄는 것입니다.

```
app.disable('x-powered-by')
```

참고

`X-Powered-By` 헤더를 비활성화하는 것만으로는 숙련된 공격자가 Express를 사용하는 앱임을 완전히 차단할 수 없습니다. 이는 단순한 공격 시도를 막는 데는 도움이 되지만, 앱이 Express로 작동함을 식별할 수 있는 다른 방법도 존재합니다.

Express는 자체 포맷의 “404 Not Found” 메시지와 포맷터 오류 응답 메시지도 전송합니다. 이러한 응답은
 [사용자 정의 404 핸들러 추가](https://expressjs.com/en/starter/faq.html#how-do-i-handle-404-responses) 및
 [사용자 정의 에러 핸들러 작성](https://expressjs.com/en/guide/error-handling.html#writing-error-handlers)을 통해 변경할 수 있습니다.

```
// last app.use calls right before app.listen():

// custom 404
app.use((req, res, next) => {
  res.status(404).send("Sorry can't find that!")
})

// custom error handler
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

## 쿠키를 안전하게 사용

쿠키로 인해 앱이 악용에 노출되지 않도록 하기 위해 기본 세션 쿠키 이름을 사용하지 말고 쿠키 보안 옵션을 적절히 설정하십시오.

두 개의 기본 미들웨어 쿠키 세션 모듈은 다음과 같습니다.

- [express-session](https://www.npmjs.com/package/express-session)(Express 3.x에서 기본 제공되는 `express.session` 미들웨어 대체).
- [cookie-session](https://www.npmjs.com/package/cookie-session)(Express 3.x에서 기본 제공되는 `express.cookieSession` 미들웨어 대체).

이 두 모듈의 주요 차이점은 쿠키 세션 데이터를 저장하는 방식입니다. [express-session](https://www.npmjs.com/package/express-session) 미들웨어는 세션 데이터를 서버에 저장하며, 쿠키 자체에는 세션 데이터가 아니라 세션 ID만 저장됩니다. 기본적으로 express-session은 인메모리 스토리지를 이용하며, 프로덕션 환경용으로 설계되지 않았습니다. 프로덕션 환경에서는 확장 가능한 session-store를 설정해야 합니다. [호환 가능한 세션 스토어](https://github.com/expressjs/session#compatible-session-stores)의 목록을 참조하십시오.

이와 반대로 [cookie-session](https://www.npmjs.com/package/cookie-session) 미들웨어는 쿠키 기반의 스토리지를 구현하며, 하나의 세션 키가 아니라 세션 전체를 쿠키에 직렬화합니다. cookie-session은 세션 데이터의 크기가 상대적으로 작으며 (오브젝트가 아닌) 원시 값으로 쉽게 인코딩 가능할 때에만 사용하십시오. 브라우저는 하나의 쿠키당 4,096바이트 이상을 지원하도록 되어 있지만, 한계를 초과하지 않도록 보장하려면 하나의 도메인당 4,093바이트의 크기를 초과하지 마십시오. 또한, 클라이언트에서 쿠키 데이터를 볼 수 있으므로, 쿠키 데이터를 안전하게 또는 모호하게 유지해야 할 이유가 있는 경우에는 express-session을 선택하는 것이 더 나을 수 있습니다.

### 기본 세션 쿠키 이름을 사용하지 않음

기본 세션 쿠키 이름을 사용하면 앱을 공격에 노출시킬 수 있습니다. 이로 인해 제기되는 보안 문제는 `X-Powered-By`와 유사하며, 잠재적인 공격자는 이를 이용해 서버의 지문을 채취한 후 이에 따라 공격 대상을 설정할 수 있습니다.

다음에는 [cookie-session](https://www.npmjs.com/package/cookie-session) 미들웨어를 사용한 예가 표시되어 있습니다.

```
const session = require('express-session')
app.set('trust proxy', 1) // trust first proxy
app.use(session({
  secret: 's3Cur3',
  name: 'sessionId'
}))
```

### 쿠키 보안 옵션 설정

다음과 같은 쿠키 옵션을 설정하여 보안을 강화하십시오.

- `secure` - 브라우저가 HTTPS를 통해서만 쿠키를 전송하도록 합니다.
- `httpOnly` - 쿠키가 클라이언트 JavaScript가 아닌 HTTP(S)를 통해서만 전송되도록 하며, 이를 통해 XSS(Cross-site scripting) 공격으로부터 보호할 수 있습니다.
- `domain` - 쿠키의 도메인을 표시합니다. URL이 요청되고 있는 서버의 도메인에 대해 비교할 때 사용하십시오. 두 도메인이 일치하는 경우에는 그 다음으로 경로 속성을 확인하십시오.
- `path` - 쿠키의 경로를 표시합니다. 요청 경로에 대해 비교할 때 사용하십시오. 이 경로와 도메인이 일치하는 경우에는 요청되고 있는 쿠키를 전송하십시오.
- `expires` - 지속적 쿠키에 대한 만기 날짜를 설정하는 데 사용됩니다.

[noCache](https://github.com/helmetjs/nocache)는 `Cache-Control` 및 Pragma 헤더를 설정하여 클라이언트 측에서 캐싱을 사용하지 않도록 합니다.

```
const session = require('cookie-session')
const express = require('express')
const app = express()

const expiryDate = new Date(Date.now() + 60 * 60 * 1000) // 1 hour
app.use(session({
  name: 'session',
  keys: ['key1', 'key2'],
  cookie: {
    secure: true,
    httpOnly: true,
    domain: 'example.com',
    path: 'foo/bar',
    expires: expiryDate
  }
}))
```

## 인증에 대한 무차별 대입 공격(Brute-force) 방지

로그인 엔드포인트를 보호하여 개인정보를 안전하게 유지해야 합니다.

간단하면서도 효과적인 방법 중 하나는 다음 두 가지 기준으로 인증 시도를 차단하는 것입니다:

1. .
2. IP 주소로부터의 오랜 시간 동안의 실패 시도 횟수입니다. 예를 들어, 하루 동안 100번의 실패 시도를 한 경우 해당 IP 주소를 차단할 수 있습니다.

[rate-limiter-flexible](https://github.com/animir/node-rate-limiter-flexible) 패키지는 이 기술을 쉽고 빠르게 구현할 수 있는 도구들을 제공합니다. [문서에서 brute-force 방지 예제](https://github.com/animir/node-rate-limiter-flexible/wiki/Overall-example#login-endpoint-protection)를 참고할 수 있습니다.

## 종속 항목이 안전한지 확인

npm을 이용해 애플리케이션의 종속 항목을 관리하는 것은 강력하면서도 편리합니다. 그러나 사용 중인 패키지에는 애플리케이션에 영향을 미칠 수 있는 치명적인 보안 취약성이 포함되어 있을 수도 있습니다. 앱의 보안성은 종속 항목 내의 “가장 약한 링크”의 보안성에 따라 결정됩니다.

npm@6부터 npm은 자동으로 모든 설치 요청을 검사합니다. 또한 `npm audit`을 이용해 여러분의 의존성 트리를 검사할 수 있습니다.

```
$ npm audit
```

더 강한 보안을 원한다면, [Snyk](https://snyk.io/)를 사용하십시오.

Snyk offers both a [command-line tool](https://www.npmjs.com/package/snyk) and a [Github 통합](https://snyk.io/docs/github) that checks your application against [Snyk’s open source vulnerability database](https://snyk.io/vuln/) for any known vulnerabilities in your dependencies. 다음과 같이 CLI을 설치합니다:

```
$ npm install -g snyk
$ cd your-app
```

아래 명령으로 애플리케이션의 취약점을 검사합니다.

```
$ snyk test
```

### 그 외의 알려져 있는 취약점 회피

Express에, 또는 앱에 사용되는 다른 모듈에 영향을 미칠 수 있는 [Node Security Project](https://npmjs.com/advisories)의 보안 권고문에 항상 주의를 기울이십시오. 일반적으로 Node Security Project는 Node의 보안과 관련된 지식 및 도구에 대한 훌륭한 자원입니다.

마지막으로, 다른 모든 웹 앱과 마찬가지로 Express 앱은 다양한 웹 기반 공격에 취약할 수 있습니다. 알려져 있는 [웹 취약성](https://www.owasp.org/www-project-top-ten/)을 숙지한 후 이러한 취약성을 피하기 위한 예방 조치를 취하십시오.

## 추가적인 고려사항

유용한 [Node.js Security Checklist](https://blog.risingstack.com/node-js-security-checklist/)에서 발췌한 몇 가지 추가적인 권장사항은 다음과 같습니다. 아래의 권장사항에 대한 모든 상세 정보를 확인하려면 해당 블로그 게시물을 참조하십시오.

- 항상 사용자 입력을 필터링하고 사용자 입력에서 민감한 데이터를 제거하여 XSS(Cross-site scripting) 및 명령 인젝션 공격으로부터 보호하십시오.
- 매개변수화된 조회 또는 준비된 명령문을 이용하여 SQL 인젝션 공격으로부터 방어하십시오.
- 오픈 소스 방식의 [sqlmap](http://sqlmap.org/) 도구를 이용하여 앱 내의 SQL 인젝션 취약성을 발견하십시오.
- [nmap](https://nmap.org/) 및 [sslyze](https://github.com/nabla-c0d3/sslyze) 도구를 이용하여 SSL 암호, 키 및 재협상의 구성, 그리고 인증서의 유효성을 테스트하십시오.
- [safe-regex](https://www.npmjs.com/package/safe-regex)를 이용하여 정규식이 [정규식 서비스 거부](https://www.owasp.org/index.php/Regular_expression_Denial_of_Service_-_ReDoS) 공격을 쉽게 받지 않도록 하십시오.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/advanced/best-practice-security.md          )

---

# Express용 템플릿 엔진 개발

> App.engine()을 사용하여 Express.js에서 사용자 정의 템플릿 엔진을 개발하는 방법을 학습합니다. 직접 템플릿 렌더링 로직을 생성하고 통합하는 예제를 함께 제공합니다.

# Express용 템플릿 엔진 개발

`app.engine(ext, callback)` 메소드를 사용하면 자신만의 템플릿 엔진을 작성할 수 있습니다. `ext`는 파일 확장자를 나타내며, `callback`은 파일의 위치, 옵션 오브젝트 및 콜백 함수 등의 항목을 매개변수로 수락하는 템플릿 엔진 함수입니다.

다음의 코드는 `.ntl` 파일을 렌더링하기 위한 매우 간단한 템플릿 엔진을 구현하는 예입니다.

```
const fs = require('fs') // this engine requires the fs module
app.engine('ntl', (filePath, options, callback) => { // define the template engine
  fs.readFile(filePath, (err, content) => {
    if (err) return callback(err)
    // this is an extremely simple template engine
    const rendered = content.toString()
      .replace('#title#', `<title>${options.title}</title>`)
      .replace('#message#', `<h1>${options.message}</h1>`)
    return callback(null, rendered)
  })
})
app.set('views', './views') // specify the views directory
app.set('view engine', 'ntl') // register the template engine
```

앱은 이제 `.ntl` 파일을 렌더링할 수 있습니다. 다음의 내용이 입력된 `index.ntl`이라는 이름의 파일을 `views` 디렉토리에 작성하십시오.

```pug
#title#
#message#
```

이후 앱에 다음과 같은 라우트를 작성하십시오.

```
app.get('/', (req, res) => {
  res.render('index', { title: 'Hey', message: 'Hello there!' })
})
```

홈 페이지에 대한 요청을 실행할 때 `index.ntl`은 HTML로 렌더링됩니다.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/advanced/developing-template-engines.md          )

---

# 상태 검사와 우아한 종료

> Express 애플리케이션에서 헬스 체크와 그레이스풀 셧다운(Graceful Shutdown)을 구현하는 방법을 학습합니다. 이 기능은 애플리케이션의 신뢰성을 향상시키고, 배포를 원활하게 관리하며, Kubernetes와 같은 로드 밸런서와의 통합을 지원합니다.

# 상태 검사와 우아한 종료

## 정상 종료

애플리케이션의 새 버전을 배포할 때, 이전 버전을 교체해야 합니다. 여러분이 사용하는 프로세스 매니저 는 애플리케어션에 SIGTERM 신호를 보내 종료를 통보할 것입니다. 애플리케이션이 신호를 받으면, 신규 요청을 받는걸 중단하고, 진행중인 요청을 끝내고, DB 연결이나 파일 사용을 포함한 사용한 리소스를 정리할 것입니다.

### Example

```
const server = app.listen(port)

process.on('SIGTERM', () => {
  debug('SIGTERM signal received: closing HTTP server')
  server.close(() => {
    debug('HTTP server closed')
  })
})
```

## Health checks

로드 밸런서는 헬스 체크를 통해 애플리케이션 인스턴스가 정상적으로 작동 중이며 요청을 수락할 수 있는지 판단합니다. For example, [Kubernetes has two health checks](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/):
로드 밸런서는 상태 확인을 애플리케이션이 장상 작동하고 요청을 받을 수 있는지 판단하는데 사용합니다.

- `liveness`: 언제 컨테이너를 재시작할지 결정합니다.
- `readiness`: 컨테이너가 트래픽을 받기 시작할 준비가 되었는지 결정합니다. 컨테이너가 준비되지 않았다면, 서비스 로드 밸런서들에게서 제거됩니다.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/advanced/healthcheck-graceful-shutdown.md          )

---

# 보안 업데이트

> Express.js의 최신 보안 업데이트와 패치 사항을 확인합니다.
각 버전에 대한 상세한 취약점 목록을 포함하여, 애플리케이션의 보안을 유지하는 데 도움이 됩니다.

# 보안 업데이트

Node.js 취약성은 Express에 직접 영향을 미칩니다. 따라서 [Node.js 취약성을 항상 주시해야 하며](https://nodejs.org
/en/blog/vulnerability/), 반드시 안정적인 최신 버전의 Node.js를 사용해야 합니다.

아래의 목록에는 지정된 버전 업데이트에서 수정된 Express 취약성이 열거되어 있습니다.

참고

Express에서 보안 취약점을 발견했다고 생각되면, [보안 정책 및 절차](https://expressjs.com/ko/resources/contributing.html#security-policies-and-procedures)를 참고해 주시기 바랍니다.

## 4.x

- 4.21.2
  - `path-to-regexp` 모듈이 [보안 취약점](https://github.com/pillarjs/path-to-regexp/security/advisories/GHSA-rhx6-c78j-4q9w)을 해결하기 위해 업데이트되었습니다.
- 4.21.1
  - `cookie` 모듈이 [보안 취약점](https://github.com/jshttp/cookie/security/advisories/GHSA-pxg6-pf52-xh8x)을 해결하기 위해 업데이트되었습니다. 이 취약점은 `res.cookie`를 사용하는 애플리케이션에 영향을 줄 수 있습니다.
- 4.20.0
  - `res.redirect`에서 발생할 수 있는 XSS 취약점이 수정되었습니다 ([권고문](https://github.com/expressjs/express/security/advisories/GHSA-qw6h-vgh9-j6wx), [CVE-2024-43796](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-43796)).
  - `serve-static` 모듈이 [보안 취약점](https://github.com/advisories/GHSA-cm22-4g7w-348p)을 해결하기 위해 업데이트되었습니다.
  - `send` 모듈이 [보안 취약점](https://github.com/advisories/GHSA-m6fv-jmcg-4jfg)을 해결하기 위해 업데이트되었습니다.
  - `path-to-regexp` 모듈이 [보안 취약점](https://github.com/pillarjs/path-to-regexp/security/advisories/GHSA-9wv6-86v2-598j)을 해결하기 위해 추가로 업데이트되었습니다.
  - `body-parser` 모듈이 [보안 취약점](https://github.com/advisories/GHSA-qwcr-r2fm-qrc7)을 해결하기 위해 업데이트되었습니다 이 취약점은 URL 인코딩이 활성화된 경우 애플리케이션에 영향을 줄 수 있습니다.
- 4.19.0, 4.19.1
  - `res.location` 및 `res.redirect`에서 발생할 수 있는 오픈 리디렉션(Open Redirect) 취약점이 수정되었습니다 ([권고문](https://github.com/expressjs/express/security/advisories/GHSA-rv95-896h-c2vc) [CVE-2024-29041](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-29041))
- 4.17.3
  - `qs` 모듈이 [보안 취약점](https://github.com/advisories/GHSA-hrpp-h998-j3pp)을 해결하기 위해 업데이트되었습니다. 이 취약점은 `req.query`, `req.body`, `req.param` API 사용 시 애플리케이션에 영향을 줄 수 있습니다.
- 4.16.0
  - 의존성 `forwarded`가 [발견된 취약점](https://npmjs.com/advisories/527)에 따라 업데이트되었습니다. `req.host`, `req.hostname`, `req.ip`, `req.ips`, `req.protocol`을 사용하는 애플리케이션에 영향을 끼칠 수 있습니다.
  - 의존성 `mime`이 [발견된 취약점](https://npmjs.com/advisories/535)에 따라 업데이트되었으나, Express에 영향을 끼치지는 않습니다.
  - 의존성 `send`가 [Node.js 8.5.0의 취약점](https://nodejs.org/en/blog/vulnerability/september-2017-path-validation/)에 대응하기 위해 업데이트되었습니다. Node.js 버전 8.5.0에서 실행되는 Express에만 영향을 끼칩니다.
- 4.15.5
  - 의존성 `debug`가 [발견된 취약점](https://snyk.io/vuln/npm:debug:20170905)에 따라 업데이트되었으나, Express에 영향을 끼치지는 않습니다.
  - 의존성 `fresh`가 [발견된 취약점](https://npmjs.com/advisories/526)에 따라 업데이트되었습니다. `express.static`, `req.fresh`, `res.json`, `res.jsonp`, `res.send`, `res.sendfile` `res.sendFile`, `res.sendStatus`를 사용하고 있는 애플리케이션에 영향을 끼칩니다.
- 4.15.3
  - 의존성 `ms`가 [발견된 취약점](https://snyk.io/vuln/npm:ms:20170412)에 따라 업데이트되었습니다. 애플리케이션이 `express.static`, `res.sendfile`, `res.sendFile`의 `maxAge` 옵션에 Untrusted 문자열을 입력받고 있으면 영향을 끼칠 수 있습니다.
- 4.15.2
  - 의존성 `qs`가 [발견된 취약점](https://snyk.io/vuln/npm:qs:20170213)에 따라 업데이트되었으나, Express에 영향을 끼치지는 않습니다. 4.15.2로 업데이트하는 것을 권장하나, 취약점을 막는 업데이트는 아닙니다..
- 4.11.1
  - `express.static`, `res.sendfile` 및 `res.sendFile`의 루트 경로 노출 취약성을 수정했습니다.
- 4.10.7
  - `express.static`의 개방된 경로 재지정 취약성을 수정했습니다([보안 권고문](https://npmjs.com/advisories/35), [CVE-2015-1164](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-1164)).
- 4.8.8
  - `express.static`의 디렉토리 조회 취약성을 수정했습니다([보안 권고문](http://npmjs.com/advisories/32), [CVE-2014-6394](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-6394)).
- 4.8.4
  - Node.js 0.10 이용 시, 특정한 상황에서 `fd` 누수가 발생할 수 있으며, 이는 `express.static` 및 `res.sendfile`에 영향을 미칩니다. 악성 요청은 `fd` 누수를 발생시킬 수 있으며, 결국 `EMFILE` 오류와 서버 무응답을 초래할 수 있습니다.
- 4.8.0
  - 조회 문자열에서 극단적으로 높은 인덱스를 갖는 스파스 배열은 프로세스가 메모리 부족을 발생시키고 서버에서 충돌이 발생하도록 하는 원인이 될 수 있습니다.
  - 극단적인 수준으로 중첩된 조회 문자열 오브젝트는 프로세스가 서버를 차단하고 일시적으로 서버를 무응답 상태로 만드는 원인이 될 수 있습니다.

## 3.x

**Express 3.x은 더 이상 유지보수되지 않습니다.**

3.x의 알려진 또는 알려지지 않은 보안 및 성능 문제는 마지막 업데이트(2015년 8월 1일) 이후로 처리되지 않고 있습니다. 최신 버전의 Express를 사용할 것을 강력히 권장합니다.

버전 3.x 이상으로 업그레이드할 수 없는 경우, [상업적 지원 옵션](https://expressjs.com/ko/support#commercial-support-options)을 고려해주시기 바랍니다.

- 3.19.1
  - `express.static`, `res.sendfile` 및 `res.sendFile`의 루트 경로 노출 취약성을 수정했습니다.
- 3.19.0
  - `express.static`의 개방된 경로 재지정 취약성을 수정했습니다([보안 권고문](https://npmjs.com/advisories/35), [CVE-2015-1164](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-1164)).
- 3.16.10
  - `express.static`의 디렉토리 조회 취약성을 수정했습니다.
- 3.16.6
  - Node.js 0.10 이용 시, 특정한 상황에서 `fd` 누수가 발생할 수 있으며, 이는 `express.static` 및 `res.sendfile`에 영향을 미칩니다. 악성 요청은 `fd` 누수를 발생시킬 수 있으며, 결국 `EMFILE` 오류와 서버 무응답을 초래할 수 있습니다.
- 3.16.0
  - 조회 문자열에서 극단적으로 높은 인덱스를 갖는 스파스 배열은 프로세스가 메모리 부족을 발생시키고 서버에서 충돌이 발생하도록 하는 원인이 될 수 있습니다.
  - 극단적인 수준으로 중첩된 조회 문자열 오브젝트는 프로세스가 서버를 차단하고 일시적으로 서버를 무응답 상태로 만드는 원인이 될 수 있습니다.
- 3.3.0
  - 지원되지 않는 메소드 대체 시도의 404 응답은 XSS(Cross-site scripting) 공격을 받기 쉬웠습니다.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/advanced/security-updates.md          )
