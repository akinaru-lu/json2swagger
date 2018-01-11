// Data types
// https://swagger.io/docs/specification/data-models/data-types/
const DataTypes = {
    Integer: 'integer',
    Number: 'number',
    String: 'string',
    Boolean: 'boolean',
    Object: 'object',
    Array: 'array',
};

function typeOf(v) {
    switch (typeof(v)) {
    case 'number':
        if (Number.isInteger(v)) {
            return DataTypes.Integer;
        }
        return DataTypes.Number;
    case 'string':
        return DataTypes.String;
    case 'boolean':
        return DataTypes.Boolean;
    case 'object':
        if (v instanceof Array) {
            return DataTypes.Array;
        }
        return DataTypes.Object;
    default:
        return typeof(v);
    }
}

// called by wrapValue
function _wrapArray(arr) {
    var wrapper = {
        "type": typeOf(arr)
    };
    if (arr.length !== 0) {
        wrapper["items"] = wrapValue(arr[0])
    }
    return wrapper;
}

// called by wrapValue
const _wrapObject = (obj) => {
    var wrapper = {
        "type": typeOf(obj)
    };
    const child = _fromObject(obj);
    if (child && Object.keys(child).length !== 0) {
        wrapper["properties"] = child;
    }
    return wrapper;
};

function wrapValue(v) {
    switch (typeOf(v)) {
    case DataTypes.Array:
        return _wrapArray(v);

    case DataTypes.Object:
        return _wrapObject(v);

    default:
        return {
            "type": typeOf(v),
            "example": v
        };
    }
}

// called by fromObject
function _fromObject(o) {
    var object = {};
    Object.keys(o).forEach(k => {
        object[k] = wrapValue(o[k]);
    })
    return object;
}

function fromObject(o) {
    switch (typeOf(o)) {
    case DataTypes.Array:
    case DataTypes.Object:
        return wrapValue(o);

    default:
        throw TypeError;
    }
}

function fromString(s) {
    return fromObject(JSON.parse(s));
}

function isNumeric(s) {
    return /^\d+(\.\d+)?$/g.exec(s) !== null
}

function formatted(v) {
    switch (typeOf(v)) {
    case DataTypes.String:
        if (v === '') {
            return "''";
        }
        if (isNumeric(v)) {
            return "'" + v + "'";
        }
        return JSON.stringify(v).slice(1, -1); // get rid of double quotes
    default:
        return JSON.stringify(v);
    }
}

function printAsYml(obj, prefix='', indent='  ') {
    if (typeof(obj) !== 'object') {
        throw TypeError("an object or array is required");
    }
    Object.keys(obj).forEach(k => {
        console.log(prefix + k + ':');
        if (typeOf(obj[k]) === DataTypes.Object) {
            printAsYml(obj[k], prefix + indent, indent);
        } else if (typeOf(obj[k]) === DataTypes.Array) {
            // since all array are wrapped to object
            // so this branch shouldn't be enter
            return;
        } else {
            console.log(prefix + indent + formatted(obj[k]));
        }
    })
}

var data = '';
process.stdin.on('data', line => {
    data += line;
});
process.stdin.on('end', () => {
    var o = fromString(data);
    printAsYml(o);
});
