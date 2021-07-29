import crypto from 'k6/crypto'

export function sign(key, msg) {
    return crypto.hmac('sha256', key, msg, 'hex')
}

function getTimestamp() {
    let timestamp = new Date()
    
    function pad(number) {
        var r = String(number)
        if (r.length === 1) {
            r = '0' + r
        }
        return r
    }
  
    return pad(timestamp.getUTCFullYear())
         + pad(timestamp.getUTCMonth() + 1)
         + pad(timestamp.getUTCDate())
         +'T'
         + pad(timestamp.getUTCHours())
         + pad(timestamp.getUTCMinutes())
         + pad(timestamp.getUTCSeconds())
         + 'Z';
}

